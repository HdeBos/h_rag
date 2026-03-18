"""Abstract base class for vector databases."""

from abc import ABC, abstractmethod

from h_rag.data_processing.embedding import Embedding
from h_rag.models.vector_search_result import VectorSearchResult


class VectorDB(ABC):
    """Abstract base class for vector databases."""

    def __init__(self) -> None:
        """Initialize the vector database."""
        self.embedding = Embedding()

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the vector database is healthy and can be reached."""
        pass

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
