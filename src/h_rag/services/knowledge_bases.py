"""Service layer for the knowledge bases router."""

from h_rag.object_storage.object_storage_factory import ObjectStorageFactory
from h_rag.vector_db.vector_db_factory import VectorDBFactory


class KnowledgeBasesService:
    """Service for handling knowledge base interactions."""

    def get_knowledge_bases(self):
        """Endpoint to get available knowledge bases."""
        vector_db = VectorDBFactory.get_vector_db()
        return vector_db.get_knowledge_bases()

    def delete_knowledge_base(self, knowledge_base_name: str):
        """Endpoint to delete a knowledge base."""
        vector_db = VectorDBFactory.get_vector_db()
        vector_db.delete(knowledge_base_name)
        object_storage = ObjectStorageFactory.get_object_storage()
        object_storage.delete_file(knowledge_base_name)

        return {"message": f"Knowledge base '{knowledge_base_name}' deleted successfully."}
