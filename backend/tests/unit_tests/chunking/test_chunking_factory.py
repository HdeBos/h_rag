"""Unit tests for the LLMFactory class."""

import pytest

from h_rag.data_processing.chunking.chunking_factory import ChunkingFactory
from h_rag.data_processing.chunking.fixed_size_chunking import FixedSizeChunking
from h_rag.data_processing.chunking.semantic_chunking import SemanticChunking


class TestChunkingFactory:
    """Test suite for the ChunkingFactory class."""

    @pytest.fixture()
    def mock_config_wrapper(self, mock_config):
        """Fixture that wraps mock_config so only return_value is required."""

        def _wrapper(return_value: str):
            mock_config(
                "h_rag.data_processing.chunking.chunking_factory",
                "chunking",
                "method",
                return_value=return_value,
            )

        return _wrapper

    def test_get_chunking_method_fixed_size(self, mock_config_wrapper) -> None:
        """Test that the factory returns a FixedSizeChunking for method 'FixedSize'."""
        mock_config_wrapper("FixedSize")
        chunking = ChunkingFactory.get_chunking_method()
        assert isinstance(chunking, FixedSizeChunking)

    def test_get_chunking_method_semantic(self, mock_config_wrapper, mock_embedding_init) -> None:
        """Test that the factory returns a SemanticChunking for method 'Semantic'."""
        mock_config_wrapper("Semantic")
        chunking = ChunkingFactory.get_chunking_method()
        assert isinstance(chunking, SemanticChunking)

    def test_get_chunking_method_unknown_raises_error(self, mock_config_wrapper) -> None:
        """Test that requesting an unknown chunking method raises ValueError."""
        mock_config_wrapper("Unknown")
        with pytest.raises(ValueError) as exc:
            ChunkingFactory.get_chunking_method()
        assert "Unknown chunking method" in str(exc.value)
