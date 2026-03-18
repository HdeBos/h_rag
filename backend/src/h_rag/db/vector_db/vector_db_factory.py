"""Factory for creating vector database instances."""

from h_rag.config.config_wrapper import get_config
from h_rag.db.vector_db.chroma_wrapper import ChromaWrapper
from h_rag.db.vector_db.pg_vector_wrapper import PgVectorWrapper
from h_rag.db.vector_db.vector_db import VectorDB
from h_rag.models.settings import get_settings


class VectorDbFactory:
    """Factory for creating vector database instances."""

    # Seperate from databases, as PgVector requires special handling due to its arguments
    _known_providers = {"Chroma", "PgVector"}

    _vector_databases = {
        "Chroma": ChromaWrapper,
        # POSSIBLE FUTURE METHODS:
        # Milvus
        # Qdrant
    }

    @classmethod
    def get_vector_db(cls) -> VectorDB:
        """Factory Method."""
        method = get_config("vector_db", "provider")
        if method not in cls._known_providers:
            raise ValueError(
                f"Unknown vector database: {method}, available methods: {list(cls._known_providers)}"
            )
        if method == "PgVector":
            settings = get_settings()
            return PgVectorWrapper(
                db_name=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password.get_secret_value(),
                host=get_config("postgres", "host"),
                port=int(get_config("postgres", "port")),
            )
        return cls._vector_databases[method]()
