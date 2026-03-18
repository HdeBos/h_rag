"""Project tools."""

import sys

import fitz
from loguru import logger

from h_rag.config.config_wrapper import get_config


def initialize_logger():
    """Initialize logger."""
    logger.remove()
    logger.add(sys.stdout, level=get_config("logger", "loguru_level"))
    logger.add("logs/info.log", level="INFO", rotation="10 MB")
    logger.add("logs/debug.log", level="DEBUG", rotation="10 MB")


def highlight_file(file_content: bytes, highlight: str) -> bytes:
    """Highlight the specified text in the file content.

    Args:
        file_content: The content of the file as bytes or string.
        highlight: The text to highlight in the file content.

    Returns:
        The file content with the specified text highlighted.
    """
    doc = fitz.open(stream=file_content, filetype="pdf")
    for page in doc:
        for quad in page.search_for(highlight, quads=True):
            page.add_highlight_annot(quad)
    return doc.tobytes()
