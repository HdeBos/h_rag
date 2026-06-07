"""Factory for creating vector database instances."""

from h_rag.config.config_wrapper import get_config
from h_rag.db.pg_vector_wrapper import PgVectorWrapper
from h_rag.models.settings import get_settings


class VectorDbFactory:
    """Factory for creating vector database instances."""

    # Seperate from databases, as PgVector requires special handling due to its arguments
    _known_providers = {"PgVector"}

    @classmethod
    def get_vector_db(cls):
        """Factory Method."""
        method = get_config("vector_db", "provider")
        if method not in cls._known_providers:
            raise ValueError(
                f"Unknown vector database: {method}, available methods: {list(cls._known_providers)}"
            )
        settings = get_settings()
        return PgVectorWrapper(
            db_name=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password.get_secret_value(),
            host=get_config("postgres", "host"),
            port=int(get_config("postgres", "port")),
        )
