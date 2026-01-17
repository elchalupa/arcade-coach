"""
Main entry point for arcade-coach.

This module initializes all components and starts the coaching loop.
Run with: python -m coach
"""

import asyncio
import os
import sys
from pathlib import Path

from colorama import init as colorama_init, Fore, Style
from dotenv import load_dotenv

from coach.config import load_config
from coach.chat import CoachBot
from coach.engine import CoachEngine
from coach.notifier import Notifier
from coach.context import ContextEngine


def print_banner():
    """Display startup banner."""
    print(f"{Fore.GREEN}")
    print("  ╔═╗┌─┐┌─┐┌─┐┬ ┬")
    print("  ║  │ │├─┤│  ├─┤")
    print("  ╚═╝└─┘┴ ┴└─┘┴ ┴")
    print(f"{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Stream Self-Care v0.1.0{Style.RESET_ALL}")
    print()


def validate_environment():
    """Check that required environment variables are set."""
    required = ["TWITCH_ACCESS_TOKEN", "TWITCH_CHANNEL", "TWITCH_USERNAME"]
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        print(f"{Fore.RED}[Error] Missing required environment variables:{Style.RESET_ALL}")
        for var in missing:
            print(f"  - {var}")
        print()
        print(f"Copy .env.example to .env and fill in your values.")
        sys.exit(1)


def main():
    """Main entry point."""
    # Initialize colorama for Windows
    colorama_init()
    
    # Show banner
    print_banner()
    
    # Load .env file from current directory or project root
    env_path = Path(".env")
    if not env_path.exists():
        env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    
    # Validate environment
    validate_environment()
    
    # Load configuration
    config_path = Path("config.yaml")
    if not config_path.exists():
        config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        config_path = Path(__file__).parent.parent / "config.example.yaml"
    
    print(f"{Fore.CYAN}[Coach]{Style.RESET_ALL} Loading configuration...")
    config = load_config(config_path)
    
    # Initialize notifier
    notifier = Notifier(config)
    
    # Initialize context engine
    context = ContextEngine(config)
    
    # Initialize coach engine
    engine = CoachEngine(config, notifier, context)
    
    # Get Twitch credentials
    token = os.getenv("TWITCH_ACCESS_TOKEN")
    channel = os.getenv("TWITCH_CHANNEL")
    username = os.getenv("TWITCH_USERNAME")
    
    # Remove "oauth:" prefix if present
    if token.startswith("oauth:"):
        token = token[6:]
    
    # Initialize and run the bot
    print(f"{Fore.CYAN}[Coach]{Style.RESET_ALL} Connecting to #{channel}...")
    print()
    
    bot = CoachBot(
        token=token,
        channel=channel,
        username=username,
        config=config,
        engine=engine,
        context=context
    )
    
    # Run the bot
    try:
        bot.run()
    except KeyboardInterrupt:
        pass
    
    # Graceful shutdown
    print()
    print(f"{Fore.CYAN}[Coach]{Style.RESET_ALL} Shutting down...")
    print(f"{Fore.CYAN}[Coach]{Style.RESET_ALL} Take care of yourself!")


if __name__ == "__main__":
    main()
