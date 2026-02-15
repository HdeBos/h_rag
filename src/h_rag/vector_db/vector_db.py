"""Abstract base class for vector databases."""

from abc import ABC, abstractmethod

from h_rag.models.vector_search_result import VectorSearchResult


class VectorDB(ABC):
    """Abstract base class for vector databases."""

    @abstractmethod
    def create(self, name: str) -> None:
        """Create a knowledge base.

        Args:
            name: The name of the knowledge base to create.
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
