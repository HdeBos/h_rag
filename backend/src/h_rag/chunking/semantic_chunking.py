"""Module for Fixed Size Chunking."""

from typing import override

import numpy as np
import spacy
from loguru import logger

from h_rag.chunking.chunking import Chunking
from h_rag.config.config_wrapper import get_config
from h_rag.vector_db.vector_db_factory import VectorDBFactory


class SemanticChunking(Chunking):
    """Chunking strategy that splits documents into semantically meaningful chunks."""

    def __init__(self):
        """Initialize the SemanticChunking class."""
        super().__init__()
        self.vector_db = VectorDBFactory.get_vector_db()

    def _split_into_sentences(self, text: str) -> list[str]:
        """Split text into sentences.

        Args:
            text: The text to split into sentences.

        Returns:
            A list of sentences extracted from the text.
        """
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        return sentences

    def _calculate_distances(self, embeddings: np.ndarray) -> list[float]:
        """Calculate cosine distances between consecutive sentence embeddings.

        Args:
            embeddings: The list of sentence embeddings.

        Returns:
            A list of cosine distances between consecutive sentence embeddings.
        """
        distances = []
        for i in range(len(embeddings) - 1):
            distance = 1 - self.vector_db.cosine_similarity(embeddings[i], embeddings[i + 1])
            distances.append(distance)
        return distances

    def _create_chunks(
        self, sentences: list[str], distances: list[float], breakpoint_threshold: float
    ) -> list[str]:
        """Create chunks based on sentence distances and a breakpoint threshold.

        Args:
            sentences: The list of sentences to chunk.
            distances: The list of cosine distances between consecutive sentence embeddings.
            breakpoint_threshold: The distance threshold above which a new chunk should be started.

        Returns:
            A list of semantically meaningful chunks.
        """
        chunks = []
        current_chunk = [sentences[0]]
        for i, distance in enumerate(distances):
            if distance > breakpoint_threshold:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i + 1]]
            else:
                current_chunk.append(sentences[i + 1])

        chunks.append(" ".join(current_chunk))
        return chunks

    @override
    def chunk(self, text: str) -> list[str]:
        logger.info("Starting semantic chunking")
        threshold_percentile = int(get_config("chunking", "semantic", "threshold_percentile"))

        sentences = self._split_into_sentences(text)
        embeddings = self.vector_db.encode(sentences, type="document")
        distances = self._calculate_distances(embeddings)
        breakpoint_threshold = float(np.percentile(distances, threshold_percentile))

        chunks = self._create_chunks(sentences, distances, breakpoint_threshold)
        return chunks
