"""Module for wrapping configuration settings."""

from pathlib import Path

import yaml


class ConfigWrapper:
    """Class for wrapping configuration settings."""

    def __init__(self):
        """Initialize the ConfigWrapper class."""
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from config.yaml."""
        path = Path(__file__).with_name("config.yaml")
        with path.open("r") as f:
            return yaml.safe_load(f)

    def get(self, key: str) -> str:
        """Get a configuration value."""
        value = self.config.get(key)
        if not value:
            raise ValueError(f"Configuration value for {key} not found")
        return value


_CONFIG = ConfigWrapper()


def get_config(key: str) -> str:
    """Get a configuration value."""
    return _CONFIG.get(key)
