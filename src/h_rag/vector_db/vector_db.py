"""Abstract base class for vector databases."""

from abc import ABC, abstractmethod
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from h_rag.config.config_wrapper import get_config
from h_rag.models.vector_search_result import VectorSearchResult


@lru_cache(maxsize=1)
def _load_embedding_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name, trust_remote_code=True)


class VectorDB(ABC):
    """Abstract base class for vector databases."""

    def __init__(self) -> None:
        """Initialize the vector database."""
        model_name = get_config("vector_db", "embedding_model")
        self.embedding_model = _load_embedding_model(model_name)

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
    def insert(self, name: str, chunks: list[str]) -> None:
        """Add chunks to a knowledge base.

        Args:
            name: The name of the knowledge base to add chunks to.
            chunks: The list of chunks to add.
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

    @abstractmethod
    def encode(self, text: str | list[str], type: str | None = None) -> np.ndarray:
        """Encode a string or a list of strings into vectors.

        Args:
            text: The string or list of strings to encode.
            type: The type of encoding, either None, "document" or "query".

        Returns:
            A numpy ndarray representing the encoded vector(s).
        """
        pass
