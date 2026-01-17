"""
Configuration loader for arcade-coach.

Loads settings from YAML config file with sensible defaults.
"""

from pathlib import Path
from typing import Any
import yaml


DEFAULT_CONFIG = {
    "timers": {
        "break_reminder_minutes": 120,
        "hydration_reminder_minutes": 45,
        "posture_reminder_minutes": 90,
        "stream_duration_alert_minutes": 240,
    },
    "context": {
        "quiet_threshold_seconds": 30,
        "hype_cooldown_seconds": 60,
        "hype_keywords": ["hype", "pog", "lets go", "amazing", "incredible"],
        "wait_for_quiet": True,
    },
    "notifications": {
        "sound": True,
        "app_name": "Coach",
        "duration": "long",
    },
    "logging": {
        "show_chat": False,
        "show_timers": True,
        "debug": False,
    },
}


def load_config(config_path: Path) -> dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Missing keys are filled with defaults.
    
    Args:
        config_path: Path to config YAML file
        
    Returns:
        Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        
        # Deep merge user config into defaults
        for section, values in user_config.items():
            if section in config and isinstance(config[section], dict):
                config[section].update(values)
            else:
                config[section] = values
    
    return config
