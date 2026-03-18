"""Unit tests for the FixedSizeChunking class."""

import pytest
from pytest_mock import MockerFixture

from h_rag.data_processing.chunking.fixed_size_chunking import FixedSizeChunking


class TestFixedSizeChunking:
    """Test suite for the FixedSizeChunking class."""

    @pytest.fixture()
    def mock_get_chunk_size(self, mocker: MockerFixture) -> MockerFixture:
        """Fixture to mock the _get_chunk_size method."""
        return mocker.patch(
            "h_rag.data_processing.chunking.fixed_size_chunking.FixedSizeChunking._get_chunk_size",
            return_value=5,
        )

    @pytest.fixture()
    def mock_get_overlap(self, mocker: MockerFixture) -> MockerFixture:
        """Fixture to mock the _get_overlap method."""
        return mocker.patch(
            "h_rag.data_processing.chunking.fixed_size_chunking.FixedSizeChunking._get_overlap",
            return_value=2,
        )

    def test_chunk(
        self, mock_get_chunk_size: MockerFixture, mock_get_overlap: MockerFixture
    ) -> None:
        """Test the chunk method for splitting text into fixed-size chunks."""
        # Arrange
        chunker = FixedSizeChunking()
        text = "abcdefghij"

        # Act
        chunks = chunker.chunk(text)

        # Assert
        assert chunks == ["abcde", "defgh", "ghij", "j"]

    def test_get_chunk_size(self, mock_config) -> None:
        """Test the _get_chunk_size method."""
        # Arrange
        mock_config(
            "h_rag.data_processing.chunking.fixed_size_chunking",
            "chunking",
            "fixed_size",
            "size",
            return_value="5",
        )
        chunker = FixedSizeChunking()

        # Act & Assert
        assert chunker._get_chunk_size() == 5

    def test_get_overlap(self, mock_config) -> None:
        """Test the _get_overlap method."""
        # Arrange
        mock_config(
            "h_rag.data_processing.chunking.fixed_size_chunking",
            "chunking",
            "fixed_size",
            "overlap",
            return_value="2",
        )
        chunker = FixedSizeChunking()

        # Act & Assert
        assert chunker._get_overlap() == 2
