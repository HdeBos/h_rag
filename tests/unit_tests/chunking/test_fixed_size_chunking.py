"""Unit tests for the FixedSizeChunking class."""

import pytest
from pytest_mock import MockerFixture

from h_rag.chunking.fixed_size_chunking import FixedSizeChunking


class TestFixedSizeChunking:
    """Test suite for the FixedSizeChunking class."""

    @pytest.fixture()
    def mock_config(self, mocker: MockerFixture):
        """Fixture to mock the get_config function with a dynamic return value."""

        def _mock(section: str, key: str, return_value: str) -> MockerFixture:
            return mocker.patch(
                "h_rag.chunking.fixed_size_chunking.get_config",
                side_effect=lambda s, k: return_value if s == section and k == key else None,
            )

        return _mock

    @pytest.fixture()
    def mock_get_chunk_size(self, mocker: MockerFixture) -> MockerFixture:
        """Fixture to mock the _get_chunk_size method."""
        return mocker.patch(
            "h_rag.chunking.fixed_size_chunking.FixedSizeChunking._get_chunk_size",
            return_value=5,
        )

    @pytest.fixture()
    def mock_get_overlap(self, mocker: MockerFixture) -> MockerFixture:
        """Fixture to mock the _get_overlap method."""
        return mocker.patch(
            "h_rag.chunking.fixed_size_chunking.FixedSizeChunking._get_overlap",
            return_value=2,
        )

    def test_chunk(
        self, mock_get_chunk_size: MockerFixture, mock_get_overlap: MockerFixture
    ) -> None:
        """Test the chunk method for splitting text into fixed-size chunks."""
        chunker = FixedSizeChunking()
        text = "abcdefghij"
        chunks = chunker.chunk(text)

        assert chunks == ["abcde", "defgh", "ghij", "j"]

    def test_get_chunk_size(self, mock_config) -> None:
        """Test the _get_chunk_size method."""
        mock_config("chunking", "size", "5")
        chunker = FixedSizeChunking()
        assert chunker._get_chunk_size() == 5

    def test_get_overlap(self, mock_config) -> None:
        """Test the _get_overlap method."""
        mock_config("chunking", "overlap", "2")
        chunker = FixedSizeChunking()
        assert chunker._get_overlap() == 2
