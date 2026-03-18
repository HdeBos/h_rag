"""Service layer for the knowledge bases router."""

import base64

from h_rag.data_processing.data_processor import DataProcessor
from h_rag.db.object_storage.object_storage_factory import ObjectStorageFactory
from h_rag.db.vector_db.vector_db_factory import VectorDbFactory
from h_rag.models.file_data import FileData
from h_rag.tools import highlight_file


class KnowledgeBasesService:
    """Service for handling knowledge base interactions."""

    def get_knowledge_bases(self) -> list[str]:
        """Endpoint to get available knowledge bases.

        Returns:
            A list of available knowledge bases from the vector database.
        """
        vector_db = VectorDbFactory.get_vector_db()
        return vector_db.get_knowledge_bases()

    def delete_knowledge_base(self, knowledge_base_name: str) -> str:
        """Endpoint to delete a knowledge base.

        Args:
            knowledge_base_name: The name of the knowledge base to delete.

        Returns:
            A message indicating the result of the deletion operation.
        """
        vector_db = VectorDbFactory.get_vector_db()
        vector_db.delete(knowledge_base_name)
        object_storage = ObjectStorageFactory.get_object_storage()
        object_storage.delete_file(knowledge_base_name)

        return f"Knowledge base '{knowledge_base_name}' deleted successfully."

    def create_knowledge_base(self, file_data: FileData) -> str:
        """Endpoint to create a knowledge base.

        Args:
            file_data: The data of the file to be processed and added to the knowledge base.

        Returns:
            The result of the knowledge base creation operation.
        """
        file_data.data = base64.b64decode(file_data.data)
        data_processor = DataProcessor()
        data = data_processor.process_file(file_data)
        data_processor.store_data(data)
        return f"Knowledge base '{file_data.name}' created successfully."

    def get_file(self, file_name: str) -> str:
        """Endpoint to retrieve a file from the knowledge base.

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
        """Endpoint to get highlighted content from a file.

        Args:
            file_name: The name of the file to retrieve.
            highlight: The text to highlight in the file.

        Returns:
            The highlighted content from the file.
        """
        object_storage = ObjectStorageFactory.get_object_storage()
        file_bytes = object_storage.get_file(file_name)
        highlighted_content = highlight_file(file_bytes, highlight)
        highlighted_content_b64 = base64.b64encode(highlighted_content).decode("utf-8")
        return highlighted_content_b64
