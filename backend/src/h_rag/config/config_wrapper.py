"""Module for wrapping configuration settings."""

from functools import lru_cache
from pathlib import Path

import yaml

from h_rag.models.settings import get_settings


class ConfigWrapper:
    """Class for wrapping configuration settings."""

    def __init__(self):
        """Initialize the ConfigWrapper class."""
        settings = get_settings()

        env = settings.app_env

        full_config = self._load_config()
        self.config = self._get_relevant_config(full_config, env)

    def _load_config(self) -> dict:
        """Load configuration from config.yaml."""
        path = Path(__file__).with_name("config.yaml")
        with path.open("r") as f:
            return yaml.safe_load(f)

    def _get_relevant_config(self, full_config: dict, env: str) -> dict:
        """Get the relevant configuration based on the environment."""
        config = full_config.get("common", {})
        env_config = full_config.get(env, {})
        config.update(env_config)
        return config

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


@lru_cache
def _get_config_wrapper() -> ConfigWrapper:
    """Get the application settings, cached for performance."""
    return ConfigWrapper()


def get_config(*keys: str) -> str:
    """Get a configuration value by traversing nested keys."""
    return _get_config_wrapper().get(*keys)
