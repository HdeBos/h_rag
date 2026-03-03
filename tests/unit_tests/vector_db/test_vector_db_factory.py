"""Unit tests for the LLMFactory class."""

import pytest

from h_rag.vector_db.chroma_wrapper import ChromaWrapper
from h_rag.vector_db.vector_db_factory import VectorDBFactory


class TestVectorDBFactory:
    """Test suite for the VectorDBFactory class."""

    @pytest.fixture()
    def mock_config_wrapper(self, mock_config):
        """Fixture that wraps mock_config so only return_value is required."""

        def _wrapper(return_value: str) -> None:
            mock_config(
                "h_rag.vector_db.vector_db_factory",
                "vector_db",
                "provider",
                return_value=return_value,
            )

        return _wrapper

    def test_get_vector_db_provider_chroma(self, mock_config_wrapper) -> None:
        """Test that the factory returns a Chroma vector DB for provider 'Chroma'."""
        mock_config_wrapper("Chroma")
        vector_db = VectorDBFactory.get_vector_db()
        assert isinstance(vector_db, ChromaWrapper)

    def test_get_vector_db_provider_unknown_raises_error(self, mock_config_wrapper) -> None:
        """Test that requesting an unknown vector DB provider raises ValueError."""
        mock_config_wrapper("Unknown")
        with pytest.raises(ValueError) as exc:
            VectorDBFactory.get_vector_db()
        assert "Unknown vector database" in str(exc.value)
