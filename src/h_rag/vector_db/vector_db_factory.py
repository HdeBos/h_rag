"""Factory for creating vector database instances."""

from h_rag.config.config_wrapper import get_config
from h_rag.vector_db.chroma_wrapper import ChromaWrapper


class VectorDBFactory:
    """Factory for creating vector database instances."""

    _vector_databases = {
        "Chroma": ChromaWrapper,
        # POSSIBLE FUTURE METHODS:
        # PGVector
        # Milvus
        # Qdrant
    }

    @classmethod
    def get_vector_db(cls) -> ChromaWrapper:
        """Factory Method."""
        method = get_config("vector_db", "provider")
        try:
            return cls._vector_databases[method]()
        except KeyError:
            raise ValueError(
                f"Unknown vector database: {method}, available methods: {list(cls._vector_databases.keys())}"
            )
