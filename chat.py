"""
Twitch chat connection for arcade-coach.

Connects to chat to monitor activity for context awareness.
Unlike heartbeat, coach doesn't track viewers - it just watches
chat flow to find good moments for reminders.
"""

from datetime import datetime
from twitchio.ext import commands
from colorama import Fore, Style

from coach.engine import CoachEngine
from coach.context import ContextEngine


class CoachBot(commands.Bot):
    """
    Twitch chat bot for context awareness.
    
    Monitors chat activity to help the coach engine find
    good moments for self-care reminders.
    """
    
    def __init__(
        self,
        token: str,
        channel: str,
        username: str,
        config: dict,
        engine: CoachEngine,
        context: ContextEngine
    ):
        """
        Initialize the Twitch bot.
        
        Args:
            token: Twitch OAuth token
            channel: Channel name to join
            username: Bot's username
            config: Configuration dictionary
            engine: Coach engine instance
            context: Context engine instance
        """
        super().__init__(
            token=token,
            prefix="!",
            initial_channels=[channel]
        )
        
        self.channel_name = channel.lower()
        self.username = username.lower()
        self.config = config
        self.engine = engine
        self.context = context
        self.show_chat = config.get("logging", {}).get("show_chat", False)
    
    async def event_ready(self):
        """Called when the bot successfully connects to Twitch."""
        print(f"{Fore.GREEN}[Coach] Connected to #{self.channel_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[Coach]{Style.RESET_ALL} Monitoring context... (Ctrl+C to stop)")
        print()
        
        # Start the coach engine's timer monitoring
        self.loop.create_task(self.engine.start_monitoring())
    
    async def event_message(self, message):
        """
        Called for every chat message.
        
        Forwards to context engine for activity tracking.
        """
        if message.echo:
            return
        
        author = message.author.name if message.author else "unknown"
        content = message.content
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Log to console if enabled
        if self.show_chat:
            print(f"{Fore.WHITE}[{timestamp}]{Style.RESET_ALL} {Fore.YELLOW}{author}{Style.RESET_ALL}: {content}")
        
        # Check if this is the streamer
        is_streamer = author.lower() == self.channel_name.lower()
        
        # Forward to context engine
        self.context.on_message(
            username=author,
            content=content,
            is_streamer=is_streamer
        )
    
    async def event_error(self, error: Exception, data: str = None):
        """Called when an error occurs."""
        print(f"{Fore.RED}[Error] {error}{Style.RESET_ALL}")
        if data:
            print(f"{Fore.RED}  Data: {data}{Style.RESET_ALL}")
