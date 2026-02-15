"""Unit tests for the LLMFactory class."""

import pytest
from pytest_mock import MockerFixture

from h_rag.vector_db.chroma_wrapper import ChromaWrapper
from h_rag.vector_db.vector_db_factory import VectorDBFactory


class TestVectorDBFactory:
    """Test suite for the VectorDBFactory class."""

    @pytest.fixture()
    def mock_config(self, mocker: MockerFixture):
        """Fixture to mock the get_config function with a dynamic return value."""

        def _mock(return_value: str):
            return mocker.patch(
                "h_rag.vector_db.vector_db_factory.get_config",
                return_value=return_value,
            )

        return _mock

    def test_get_vector_db_provider_chroma(self, mock_config) -> None:
        """Test that the factory returns a Chroma vector DB for provider 'Chroma'."""
        mock_config("Chroma")
        vector_db = VectorDBFactory.get_vector_db()
        assert isinstance(vector_db, ChromaWrapper)

    def test_get_vector_db_provider_unknown_raises_error(self, mock_config) -> None:
        """Test that requesting an unknown vector DB provider raises ValueError."""
        mock_config("Unknown")
        with pytest.raises(ValueError) as exc:
            VectorDBFactory.get_vector_db()
        assert "Unknown vector database" in str(exc.value)
