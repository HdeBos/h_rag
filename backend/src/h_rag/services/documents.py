"""Service layer for the knowledge bases router."""

import base64

from loguru import logger

from h_rag.db.pg_vector_wrapper import PgVectorWrapper
from h_rag.db.postgres_wrapper import PostgresWrapper
from h_rag.object_storage.object_storage_factory import ObjectStorageFactory
from h_rag.tools import highlight_file


class DocumentsService:
    """Service for handling document interactions."""

    def __init__(self, postgres_wrapper: PostgresWrapper):
        """Initialize the documents service."""
        self._pg = postgres_wrapper

    def list_files(self) -> list[str]:
        """List all files in the knowledge base.

        Returns:
            A list of file names available in the knowledge base.
        """
        document_store = PgVectorWrapper(self._pg)
        return document_store.get_documents()

    def get_file(self, file_name: str) -> str:
        """Retrieve a file from the knowledge base.

        Args:
            file_name: The name of the file to retrieve.

        Returns:
            The base64-encoded string of the requested file.
        """
        object_storage = ObjectStorageFactory.get_object_storage()

        file_bytes = object_storage.get_file(file_name)
        file_b64 = base64.b64encode(file_bytes).decode("utf-8")
        return file_b64

    def get_highlighted_file(self, file_name: str, highlight: str) -> str:
        """Get highlighted content from a file.

        Args:
            file_name: The name of the file to retrieve.
            highlight: The text to highlight in the file.

        Returns:
            The highlighted content from the file.
        """
        logger.info(f"Retrieving file {file_name} for highlighting")
        object_storage = ObjectStorageFactory.get_object_storage()
        file_bytes = object_storage.get_file(file_name)
        highlighted_content = highlight_file(file_bytes, highlight)
        highlighted_content_b64 = base64.b64encode(highlighted_content).decode("utf-8")
        return highlighted_content_b64
