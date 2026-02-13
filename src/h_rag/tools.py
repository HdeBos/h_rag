"""Project tools."""

import sys

from dotenv import load_dotenv
from loguru import logger

from h_rag.config.config_wrapper import get_config


def load_env():
    """Load environment variables from .env file."""
    load_dotenv(override=True)


def initialize_logger():
    """Initialize logger."""
    logger.remove()
    logger.add(sys.stdout, level=get_config("loguru_level"))
    logger.add("logs/info.log", level="INFO", rotation="10 MB")
    logger.add("logs/debug.log", level="DEBUG", rotation="10 MB")
