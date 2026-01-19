"""
Coach engine for arcade-coach.

Manages self-care timers and decides when to send reminders
based on context awareness.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional
from colorama import Fore, Style

from coach.notifier import Notifier
from coach.context import ContextEngine


class Timer:
    """Represents a single self-care timer."""
    
    def __init__(self, name: str, interval_minutes: int, message: str):
        self.name = name
        self.interval = timedelta(minutes=interval_minutes)
        self.message = message
        self.last_triggered: Optional[datetime] = None
        self.started_at: datetime = datetime.now()
        self.pending: bool = False  # True if due but waiting for good moment
    
    def is_due(self) -> bool:
        """Check if this timer is due to fire."""
        now = datetime.now()
        
        if self.last_triggered is None:
            # First trigger: based on start time
            return (now - self.started_at) >= self.interval
        else:
            return (now - self.last_triggered) >= self.interval
    
    def trigger(self):
        """Mark timer as triggered."""
        self.last_triggered = datetime.now()
        self.pending = False
    
    def time_until_due(self) -> timedelta:
        """Get time remaining until timer is due."""
        now = datetime.now()
        
        if self.last_triggered is None:
            next_due = self.started_at + self.interval
        else:
            next_due = self.last_triggered + self.interval
        
        remaining = next_due - now
        return remaining if remaining.total_seconds() > 0 else timedelta(0)


class CoachEngine:
    """
    The coach engine manages self-care timers.
    
    Timers:
    - Break reminder (default: 2 hours)
    - Hydration nudge (default: 45 min)
    - Posture check (default: 90 min)
    - Stream duration alert (default: 4 hours)
    """
    
    def __init__(
        self,
        config: dict,
        notifier: Notifier,
        context: ContextEngine
    ):
        """
        Initialize the coach engine.
        
        Args:
            config: Configuration dictionary
            notifier: Notification system instance
            context: Context engine instance
        """
        self.config = config
        self.notifier = notifier
        self.context = context
        
        self.debug = config.get("logging", {}).get("debug", False)
        self.show_timers = config.get("logging", {}).get("show_timers", True)
        
        # Load timer settings
        timer_config = config.get("timers", {})
        
        # Initialize timers
        self.timers: list[Timer] = []
        
        # Break reminder
        break_mins = timer_config.get("break_reminder_minutes", 120)
        if break_mins > 0:
            self.timers.append(Timer(
                name="break",
                interval_minutes=break_mins,
                message="Time for a break! Stand up, stretch, rest your eyes."
            ))
        
        # Hydration reminder
        hydration_mins = timer_config.get("hydration_reminder_minutes", 45)
        if hydration_mins > 0:
            self.timers.append(Timer(
                name="hydration",
                interval_minutes=hydration_mins,
                message="Stay hydrated! Take a sip of water."
            ))
        
        # Posture reminder
        posture_mins = timer_config.get("posture_reminder_minutes", 90)
        if posture_mins > 0:
            self.timers.append(Timer(
                name="posture",
                interval_minutes=posture_mins,
                message="Posture check! Sit up straight, relax your shoulders."
            ))
        
        # Stream duration alert
        duration_mins = timer_config.get("stream_duration_alert_minutes", 240)
        if duration_mins > 0:
            self.timers.append(Timer(
                name="duration",
                interval_minutes=duration_mins,
                message="You've been streaming for a while. Consider wrapping up soon."
            ))
        
        # Stream start time
        self.stream_start = datetime.now()
        
        # Monitoring task handle
        self._monitoring_task: Optional[asyncio.Task] = None
    
    async def start_monitoring(self):
        """
        Start the background timer monitoring loop.
        """
        self._monitoring_task = asyncio.current_task()
        
        if self.debug:
            print(f"{Fore.BLUE}[Debug] Starting timer monitoring{Style.RESET_ALL}")
        
        # Show initial timer status
        if self.show_timers:
            self._print_timer_status()
        
        try:
            while True:
                await self._check_timers()
                await asyncio.sleep(10)  # Check every 10 seconds
        except asyncio.CancelledError:
            if self.debug:
                print(f"{Fore.BLUE}[Debug] Timer monitoring stopped{Style.RESET_ALL}")
            raise
    
    async def stop_monitoring(self):
        """Stop the timer monitoring loop gracefully."""
        if self._monitoring_task is None:
            return
        
        self._monitoring_task.cancel()
        try:
            await self._monitoring_task
        except asyncio.CancelledError:
            pass
        
        self._monitoring_task = None
    
    async def _check_timers(self):
        """Check all timers and send notifications when appropriate."""
        for timer in self.timers:
            if timer.is_due() or timer.pending:
                timer.pending = True
                
                # Check if it's a good moment
                if self.context.is_good_moment():
                    self._trigger_timer(timer)
                elif self.debug:
                    print(f"{Fore.BLUE}[Debug] {timer.name} pending, waiting for good moment{Style.RESET_ALL}")
    
    def _trigger_timer(self, timer: Timer):
        """
        Trigger a timer notification.
        
        Args:
            timer: The timer to trigger
        """
        if self.show_timers:
            print(f"{Fore.GREEN}[Coach]{Style.RESET_ALL} → {timer.name.capitalize()} reminder")
        
        # Send notification
        self.notifier.notify_reminder(
            reminder_type=timer.name,
            message=timer.message
        )
        
        timer.trigger()
    
    def _print_timer_status(self):
        """Print current timer status to console."""
        print(f"{Fore.CYAN}[Coach]{Style.RESET_ALL} Active timers:")
        for timer in self.timers:
            remaining = timer.time_until_due()
            mins = int(remaining.total_seconds() / 60)
            print(f"  - {timer.name.capitalize()}: {mins} min remaining")
        print()
    
    def get_stream_duration(self) -> timedelta:
        """Get how long the stream has been running."""
        return datetime.now() - self.stream_start
    
    def reset_timer(self, timer_name: str):
        """
        Reset a specific timer.
        
        Args:
            timer_name: Name of timer to reset
        """
        for timer in self.timers:
            if timer.name == timer_name:
                timer.last_triggered = datetime.now()
                timer.pending = False
                if self.show_timers:
                    print(f"{Fore.CYAN}[Coach]{Style.RESET_ALL} Reset {timer_name} timer")
                break
