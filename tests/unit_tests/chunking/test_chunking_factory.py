"""Unit tests for the LLMFactory class."""

import pytest
from pytest_mock import MockerFixture

from h_rag.chunking.chunking_factory import ChunkingFactory
from h_rag.chunking.fixed_size_chunking import FixedSizeChunking


class TestChunkingFactory:
    """Test suite for the ChunkingFactory class."""

    @pytest.fixture()
    def mock_config(self, mocker: MockerFixture):
        """Fixture to mock the get_config function with a dynamic return value."""

        def _mock(return_value: str):
            return mocker.patch(
                "h_rag.chunking.chunking_factory.get_config",
                return_value=return_value,
            )

        return _mock

    def test_get_chunking_method_fixed_size(self, mock_config) -> None:
        """Test that the factory returns a FixedSizeChunking for method 'FixedSize'."""
        mock_config("FixedSize")
        chunking = ChunkingFactory.get_chunking_method()
        assert isinstance(chunking, FixedSizeChunking)

    def test_get_chunking_method_unknown_raises_error(self, mock_config) -> None:
        """Test that requesting an unknown chunking method raises ValueError."""
        mock_config("Unknown")
        with pytest.raises(ValueError) as exc:
            ChunkingFactory.get_chunking_method()
        assert "Unknown chunking method" in str(exc.value)
