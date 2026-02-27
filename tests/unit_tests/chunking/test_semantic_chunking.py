"""Unit tests for the SemanticChunking class."""

import numpy as np
from pytest_mock import MockerFixture

from h_rag.chunking.semantic_chunking import SemanticChunking


class TestSemanticChunking:
    """Test suite for the SemanticChunking class."""

    def test_split_into_sentences(self) -> None:
        """Test the _split_into_sentences method for splitting text into sentences."""
        # Arrange
        chunker = SemanticChunking()
        text = "This is the first sentence. This is the second sentence! Is this the third sentence? Yes, it is."

        # Act
        sentences = chunker._split_into_sentences(text)

        # Assert
        assert sentences == [
            "This is the first sentence.",
            "This is the second sentence!",
            "Is this the third sentence?",
            "Yes, it is.",
        ]

    def test_calculate_distances(self, mocker: MockerFixture) -> None:
        """Test the _calculate_distances method for calculating cosine distances between sentence embeddings."""
        # Arrange
        chunker = SemanticChunking()
        embeddings = np.array([[1, 0], [0, 1], [1, 1]])
        mock_cosine_similarity = mocker.patch.object(
            chunker.vector_db, "cosine_similarity", side_effect=[0.0, 0.5]
        )

        # Act
        distances = chunker._calculate_distances(embeddings)

        # Assert
        assert distances == [1.0, 0.5]
        assert mock_cosine_similarity.call_count == 2

    def test_create_chunks(self) -> None:
        """Test the _create_chunks method for creating chunks based on sentence distances and a breakpoint threshold."""
        # Arrange
        chunker = SemanticChunking()
        sentences = [
            "This is the first sentence.",
            "This is the second sentence!",
            "Is this the third sentence?",
            "Yes, it is.",
        ]
        distances = [0.1, 0.5, 0.2]
        breakpoint_threshold = 0.3

        # Act
        chunks = chunker._create_chunks(sentences, distances, breakpoint_threshold)

        # Assert
        assert chunks == [
            "This is the first sentence. This is the second sentence!",
            "Is this the third sentence? Yes, it is.",
        ]

    def test_chunk(self, mocker: MockerFixture, mock_config) -> None:
        """Test the chunk method for end-to-end chunking of text."""
        # Arrange
        chunker = SemanticChunking()
        text = "This is the first sentence. This is the second sentence! Is this the third sentence? Yes, it is."
        mock_split_into_sentences = mocker.patch.object(
            chunker,
            "_split_into_sentences",
            return_value=[
                "This is the first sentence.",
                "This is the second sentence!",
                "Is this the third sentence?",
                "Yes, it is.",
            ],
        )
        mock_encode = mocker.patch.object(
            chunker.vector_db, "encode", return_value=np.array([[1, 0], [0, 1], [1, 1], [0.5, 0.5]])
        )
        mock_config(
            "h_rag.chunking.semantic_chunking",
            "chunking",
            "semantic",
            "threshold_percentile",
            return_value="25",
        )
        mock_cosine_similarity = mocker.patch.object(
            chunker.vector_db, "cosine_similarity", side_effect=[0.0, 0.1, 0.9]
        )

        # Act
        chunks = chunker.chunk(text)

        # Assert
        assert chunks == [
            "This is the first sentence.",
            "This is the second sentence!",
            "Is this the third sentence? Yes, it is.",
        ]
        assert mock_split_into_sentences.call_once_with(text)
        assert mock_encode.call_once_with(
            [
                "This is the first sentence.",
                "This is the second sentence!",
                "Is this the third sentence?",
                "Yes, it is.",
            ],
            type="document",
        )
        assert mock_cosine_similarity.call_count == 3
