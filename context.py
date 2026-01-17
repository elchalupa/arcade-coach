"""
Context engine for arcade-coach.

Tracks chat activity and hype levels to determine when it's
a good moment to send reminders. Never interrupt a moment.
"""

from datetime import datetime, timedelta
from typing import Optional
from colorama import Fore, Style


class ContextEngine:
    """
    Tracks stream context to find good moments for reminders.
    
    Philosophy: Never interrupt a hype moment. Wait for quiet.
    
    Tracks:
    - Time since last chat message
    - Recent hype keywords
    - Chat velocity (messages per minute)
    """
    
    def __init__(self, config: dict):
        """
        Initialize the context engine.
        
        Args:
            config: Configuration dictionary
        """
        context_config = config.get("context", {})
        
        self.quiet_threshold = context_config.get("quiet_threshold_seconds", 30)
        self.hype_cooldown = context_config.get("hype_cooldown_seconds", 60)
        self.hype_keywords = [kw.lower() for kw in context_config.get("hype_keywords", [])]
        self.wait_for_quiet = context_config.get("wait_for_quiet", True)
        
        self.debug = config.get("logging", {}).get("debug", False)
        
        # State tracking
        self.last_message_time: datetime = datetime.now()
        self.last_hype_time: Optional[datetime] = None
        self.message_times: list[datetime] = []  # Rolling window for velocity
    
    def on_message(self, username: str, content: str, is_streamer: bool = False):
        """
        Process an incoming chat message for context.
        
        Args:
            username: The username of the chatter
            content: The message content
            is_streamer: Whether this message is from the channel owner
        """
        now = datetime.now()
        self.last_message_time = now
        
        # Track message times for velocity calculation
        self.message_times.append(now)
        
        # Prune old messages (keep last 5 minutes)
        cutoff = now - timedelta(minutes=5)
        self.message_times = [t for t in self.message_times if t > cutoff]
        
        # Check for hype keywords
        content_lower = content.lower()
        for keyword in self.hype_keywords:
            if keyword in content_lower:
                self.last_hype_time = now
                if self.debug:
                    print(f"{Fore.BLUE}[Debug] Hype detected: {keyword}{Style.RESET_ALL}")
                break
    
    def is_good_moment(self) -> bool:
        """
        Check if this is a good moment to send a reminder.
        
        Returns:
            True if it's a good moment (quiet, no recent hype)
        """
        if not self.wait_for_quiet:
            return True
        
        now = datetime.now()
        
        # Check if chat is quiet
        seconds_since_message = (now - self.last_message_time).total_seconds()
        is_quiet = seconds_since_message >= self.quiet_threshold
        
        # Check if we're past hype cooldown
        if self.last_hype_time is not None:
            seconds_since_hype = (now - self.last_hype_time).total_seconds()
            past_hype = seconds_since_hype >= self.hype_cooldown
        else:
            past_hype = True
        
        if self.debug:
            print(f"{Fore.BLUE}[Debug] Context check: quiet={is_quiet}, past_hype={past_hype}{Style.RESET_ALL}")
        
        return is_quiet and past_hype
    
    def get_messages_per_minute(self) -> float:
        """
        Calculate current chat velocity.
        
        Returns:
            Messages per minute over the last 5 minutes
        """
        if not self.message_times:
            return 0.0
        
        now = datetime.now()
        cutoff = now - timedelta(minutes=5)
        recent = [t for t in self.message_times if t > cutoff]
        
        if not recent:
            return 0.0
        
        # Calculate time span
        time_span = (now - recent[0]).total_seconds() / 60
        if time_span < 0.1:
            return 0.0
        
        return len(recent) / time_span
    
    def seconds_since_last_message(self) -> float:
        """Get seconds since the last chat message."""
        return (datetime.now() - self.last_message_time).total_seconds()
