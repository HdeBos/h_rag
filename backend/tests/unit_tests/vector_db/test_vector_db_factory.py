"""Unit tests for the LLMFactory class."""

import pytest
from pytest_mock import MockerFixture

from h_rag.db.vector_db.chroma_wrapper import ChromaWrapper
from h_rag.db.vector_db.pg_vector_wrapper import PgVectorWrapper
from h_rag.db.vector_db.vector_db_factory import VectorDbFactory


class TestVectorDBFactory:
    """Test suite for the VectorDbFactory class."""

    @pytest.fixture()
    def mock_config_wrapper(self, mock_config):
        """Fixture that wraps mock_config so only return_value is required."""

        def _wrapper(return_value: str) -> None:
            mock_config(
                "h_rag.db.vector_db.vector_db_factory",
                "vector_db",
                "provider",
                return_value=return_value,
            )

        return _wrapper

    def test_get_vector_db_provider_chroma(self, mock_config_wrapper, mock_embedding_init) -> None:
        """Test that the factory returns a Chroma vector DB for provider 'Chroma'."""
        mock_config_wrapper("Chroma")
        vector_db = VectorDbFactory.get_vector_db()
        assert isinstance(vector_db, ChromaWrapper)

    def test_get_vector_db_provider_pgvector(
        self, mocker: MockerFixture, mock_embedding_init
    ) -> None:
        """Test that the factory returns a PgVector vector DB for provider 'PgVector'."""
        config_values = {
            ("vector_db", "provider"): "PgVector",
            ("postgres", "host"): "localhost",
            ("postgres", "port"): "5432",
        }
        mocker.patch(
            "h_rag.db.vector_db.vector_db_factory.get_config",
            side_effect=lambda *args: config_values.get(args),
        )
        mock_settings = mocker.Mock()
        mock_settings.postgres_db = "test_db"
        mock_settings.postgres_user = "test_user"
        mock_settings.postgres_password.get_secret_value.return_value = "test_password"
        mocker.patch(
            "h_rag.db.vector_db.vector_db_factory.get_settings", return_value=mock_settings
        )
        mocker.patch.object(PgVectorWrapper, "__init__", return_value=None)
        vector_db = VectorDbFactory.get_vector_db()
        assert isinstance(vector_db, PgVectorWrapper)

    def test_get_vector_db_provider_unknown_raises_error(self, mock_config_wrapper) -> None:
        """Test that requesting an unknown vector DB provider raises ValueError."""
        mock_config_wrapper("Unknown")
        with pytest.raises(ValueError) as exc:
            VectorDbFactory.get_vector_db()
        assert "Unknown vector database" in str(exc.value)
