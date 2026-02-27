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

    def get(self, *keys: str) -> str:
        """Get a configuration value by traversing nested keys.

        Supports arbitrary depth, e.g. get("chunking", "semantic", "threshold_percentile").
        """
        if not keys:
            raise ValueError("At least one key must be provided")
        current: dict | str = self.config
        for key in keys:
            if not isinstance(current, dict):
                raise ValueError(f"Cannot traverse into non-dict value at key '{key}'")
            value = current.get(key)
            if value is None:
                raise ValueError(f"Configuration key '{key}' not found")
            current = value
        if isinstance(current, dict):
            raise ValueError(f"Configuration value at keys {keys} is not a string")
        return current


_CONFIG = ConfigWrapper()


def get_config(*keys: str) -> str:
    """Get a configuration value by traversing nested keys."""
    return _CONFIG.get(*keys)
