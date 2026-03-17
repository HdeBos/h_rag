"""Pydantic settings model for application configuration, loading .env data."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    gemini_api_key: str

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    bucket_name: str

    model_config = SettingsConfigDict(env_file=".env")
