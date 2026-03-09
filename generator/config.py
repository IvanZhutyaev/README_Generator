"""Configuration management for README Generator Pro."""

import json
import os
from typing import Dict, Any, Optional
from .utils import get_package_dir

# Default configuration values
DEFAULT_CONFIG = {
    'lang': 'en',
    'template': 'default',
    'output': 'README.md',
    'sections': ['installation', 'usage', 'license'],
    'section_data': {},
    'python_version': '3.6+'
}


class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass


class ConfigNotFoundError(ConfigError):
    """Raised when config file is not found."""
    pass


class ConfigInvalidError(ConfigError):
    """Raised when config file is invalid."""
    pass


def load_config(path: str) -> Dict[str, Any]:
    """
    Load JSON configuration from file.

    Args:
        path: Path to JSON config file

    Returns:
        Dictionary with configuration

    Raises:
        ConfigNotFoundError: If file not found
        ConfigInvalidError: If JSON is invalid
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ConfigNotFoundError(f"Config file not found: {path}")
    except json.JSONDecodeError as e:
        raise ConfigInvalidError(f"Invalid JSON in config file: {e}")


def save_config(path: str, config: Dict[str, Any]) -> None:
    """
    Save configuration to JSON file.

    Args:
        path: Path to save config file
        config: Configuration dictionary

    Raises:
        ConfigError: If unable to write file
    """
    try:
        # Create directory if it doesn't exist
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False, sort_keys=True)
    except IOError as e:
        raise ConfigError(f"Unable to save config: {e}")


def merge_with_defaults(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge user configuration with defaults.

    Args:
        config: User configuration dictionary

    Returns:
        Merged configuration with defaults
    """
    merged = DEFAULT_CONFIG.copy()
    merged.update(config)

    # Ensure sections is a list
    if 'sections' in merged and isinstance(merged['sections'], str):
        merged['sections'] = [s.strip() for s in merged['sections'].split(',')]

    # Ensure section_data exists
    if 'section_data' not in merged:
        merged['section_data'] = {}

    return merged


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure.

    Args:
        config: Configuration dictionary to validate

    Returns:
        True if valid, False otherwise
    """
    required_keys = ['lang', 'template', 'output']

    # Check required keys
    for key in required_keys:
        if key not in config:
            return False

    # Check lang value
    if config['lang'] not in ['en', 'ru']:
        return False

    # Check sections is list
    if 'sections' in config and not isinstance(config['sections'], list):
        return False

    return True


def get_config_path(filename: str = 'config.json') -> str:
    """
    Get path to configuration file in user's home directory.

    Args:
        filename: Configuration filename

    Returns:
        Full path to config file
    """
    home = os.path.expanduser('~')
    config_dir = os.path.join(home, '.config', 'readme-generator')
    return os.path.join(config_dir, filename)