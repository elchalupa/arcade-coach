"""
Cross-platform notification system for arcade-coach.

Detects the operating system and uses the appropriate backend:
- Windows: winotify (native toast notifications)
- macOS/Linux: plyer (cross-platform notifications)
"""

import sys
from typing import Optional

PLATFORM = sys.platform

if PLATFORM == "win32":
    try:
        from winotify import Notification, audio
        BACKEND = "winotify"
    except ImportError:
        BACKEND = None
else:
    try:
        from plyer import notification as plyer_notification
        BACKEND = "plyer"
    except ImportError:
        BACKEND = None


class Notifier:
    """
    Handles sending native notifications across platforms.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the notifier.
        
        Args:
            config: Configuration dictionary
        """
        notif_config = config.get("notifications", {})
        
        self.app_name = notif_config.get("app_name", "Coach")
        self.sound_enabled = notif_config.get("sound", True)
        self.duration = notif_config.get("duration", "long")
        self.timeout_seconds = 10 if self.duration == "long" else 5
        
        if BACKEND is None:
            from colorama import Fore, Style
            if PLATFORM == "win32":
                print(f"{Fore.YELLOW}[Coach]{Style.RESET_ALL} winotify not installed, notifications disabled")
            else:
                print(f"{Fore.YELLOW}[Coach]{Style.RESET_ALL} plyer not installed, notifications disabled")
    
    def _send(self, title: str, message: str):
        """Send a notification using the platform-appropriate backend."""
        if BACKEND is None:
            return
        
        if BACKEND == "winotify":
            self._send_winotify(title, message)
        elif BACKEND == "plyer":
            self._send_plyer(title, message)
    
    def _send_winotify(self, title: str, message: str):
        """Send notification via winotify (Windows)."""
        toast = Notification(
            app_id=self.app_name,
            title=title,
            msg=message,
            duration=self.duration
        )
        
        if self.sound_enabled:
            toast.set_audio(audio.Default, loop=False)
        
        toast.show()
    
    def _send_plyer(self, title: str, message: str):
        """Send notification via plyer (macOS/Linux)."""
        try:
            plyer_notification.notify(
                title=title,
                message=message,
                app_name=self.app_name,
                timeout=self.timeout_seconds
            )
        except Exception:
            pass
    
    def notify_reminder(self, reminder_type: str, message: str):
        """
        Send a self-care reminder notification.
        
        Args:
            reminder_type: Type of reminder (break, hydration, posture, duration)
            message: The reminder message
        """
        titles = {
            "break": "Break Time",
            "hydration": "Hydration Check",
            "posture": "Posture Check",
            "duration": "Stream Duration",
        }
        
        title = titles.get(reminder_type, "Reminder")
        self._send(title, message)
    
    def notify_custom(self, title: str, message: str):
        """Send a custom notification."""
        self._send(title, message)
