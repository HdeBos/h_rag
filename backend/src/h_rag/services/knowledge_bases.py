"""Service layer for the knowledge bases router."""

import base64

from loguru import logger

from h_rag.data_processing.data_processor import DataProcessor
from h_rag.db.pg_vector_wrapper import PgVectorWrapper
from h_rag.db.postgres_wrapper import PostgresWrapper
from h_rag.models.file_data import FileData
from h_rag.object_storage.object_storage_factory import ObjectStorageFactory


class KnowledgeBasesService:
    """Service for handling knowledge base interactions."""

    def __init__(self, postgres_wrapper: PostgresWrapper):
        """Initialize the knowledge bases service."""
        self._pg = postgres_wrapper

    def get_knowledge_bases(self) -> list[str]:
        """Get available knowledge bases.

        Returns:
            A list of available knowledge bases from the vector database.
        """
        knowledge_base_store = PgVectorWrapper(self._pg)
        return knowledge_base_store.get_knowledge_bases()

    def delete_knowledge_base(self, knowledge_base_name: str) -> None:
        """Delete a knowledge base.

        Args:
            knowledge_base_name: The name of the knowledge base to delete.
        """
        knowledge_base_store = PgVectorWrapper(self._pg)
        knowledge_base_store.delete(knowledge_base_name)
        logger.info(f"Deleted knowledge base '{knowledge_base_name}''")
        object_storage = ObjectStorageFactory.get_object_storage()
        object_storage.delete_file(knowledge_base_name)
        logger.info(f"Deleted '{knowledge_base_name}' from object storage")

    def create_knowledge_base(self, file_data: FileData) -> str:
        """Create a knowledge base.

        Args:
            file_data: The data of the file to be processed and added to the knowledge base.

        Returns:
            The result of the knowledge base creation operation.
        """
        file_data.data = base64.b64decode(file_data.data)
        data_processor = DataProcessor()
        data = data_processor.process_file(file_data)
        data_processor.store_data(self._pg, data)
        return f"Knowledge base '{file_data.name}' created successfully."

    def add_document_to_knowledge_base(self, knowledge_base_name: str, file_name: str) -> str:
        """Add a document to an existing knowledge base.

        Args:
            knowledge_base_name: The name of the knowledge base to add the document to.
            file_name: The name of the document to add.

        Returns:
            The result of the document addition operation.
        """
        knowledge_base_store = PgVectorWrapper(self._pg)
        knowledge_base_store.add_document_to_kb(knowledge_base_name, file_name)
        return (
            f"Document '{file_name}' added to knowledge base '{knowledge_base_name}' successfully."
        )

    def remove_document_from_knowledge_base(self, knowledge_base_name: str, file_name: str) -> None:
        """Remove a document from a knowledge base.

        Args:
            knowledge_base_name: The name of the knowledge base to remove the document from.
            file_name: The name of the document to remove.
        """
        knowledge_base_store = PgVectorWrapper(self._pg)
        knowledge_base_store.remove_document_from_kb(knowledge_base_name, file_name)
