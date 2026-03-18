"""Pydantic settings model for application configuration, loading .env data."""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    gemini_api_key: SecretStr

    # Garage Object Storage settings
    aws_access_key_id: str
    aws_secret_access_key: SecretStr
    aws_region: str
    bucket_name: str

    # PostgreSQL settings
    postgres_user: str
    postgres_password: SecretStr
    postgres_db: str

    # Flag to indicate if running in Docker
    app_env: str = "local"

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"), env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """Get the application settings, cached for performance."""
    return Settings()  # type: ignore
