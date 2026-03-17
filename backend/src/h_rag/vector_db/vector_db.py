"""Abstract base class for vector databases."""

from abc import ABC, abstractmethod
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from h_rag.config.config_wrapper import get_config
from h_rag.models.vector_search_result import VectorSearchResult


@lru_cache(maxsize=1)
def _load_embedding_model(model_name: str, revision: str) -> SentenceTransformer:
    return SentenceTransformer(model_name, trust_remote_code=True, revision=revision)


class VectorDB(ABC):
    """Abstract base class for vector databases."""

    def __init__(self) -> None:
        """Initialize the vector database."""
        model_name = get_config("vector_db", "embedding_model", "name")
        revision = get_config("vector_db", "embedding_model", "revision")
        self.embedding_model = _load_embedding_model(model_name, revision)

    @abstractmethod
    def create(self, name: str) -> None:
        """Create a knowledge base.

        Args:
            name: The name of the knowledge base to create.
        """
        pass

    @abstractmethod
    def delete(self, name: str) -> None:
        """Delete a knowledge base.

        Args:
            name: The name of the knowledge base to delete.
        """
        pass

    @abstractmethod
    def insert(
        self,
        name: str,
        chunks: list[str],
        doc_name: str,
        pages: list[int],
    ) -> None:
        """Add chunks to a knowledge base.

        Args:
            name: The name of the knowledge base to add chunks to.
            chunks: The list of chunks to add.
            doc_name: The name of the document the chunks belong to.
            pages: The list of page numbers corresponding to each chunk.
        """
        pass

    @abstractmethod
    def query(self, name: str, query: str, n_results: int = 5) -> list["VectorSearchResult"]:
        """Query a knowledge base.

        Args:
            name: The name of the knowledge base to query.
            query: The query string to search for.
            n_results: The number of results to return.

        Returns:
            A list of results from the knowledge base.
        """
        pass

    @abstractmethod
    def get_knowledge_bases(self) -> list[str]:
        """Get all knowledge bases.

        Returns:
            A list of all knowledge bases.
        """
        pass

    def encode(self, text: str | list[str], type: str) -> np.ndarray:
        """Encode a string or a list of strings into vectors.

        Args:
            text: The string or list of strings to encode.
            type: The type of encoding, either "document" or "query".

        Returns:
            A numpy ndarray representing the encoded vector(s).
        """
        model_name = get_config("vector_db", "embedding_model", "name")
        if model_name == "nomic-ai/nomic-embed-text-v1.5":
            text = (
                f"search_{type}:" + text
                if isinstance(text, str)
                else [f"search_{type}:" + t for t in text]
            )
        embeddings = self.embedding_model.encode(text)
        return np.asarray(embeddings, dtype=float)

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors.

        Args:
            vec1: The first vector.
            vec2: The second vector.

        Returns:
            The cosine similarity between the two vectors.
        """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
