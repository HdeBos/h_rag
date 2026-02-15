"""ABC for document chunking strategies for retrieval-augmented generation (RAG) systems."""

from abc import ABC, abstractmethod


class Chunking(ABC):
    """Base class for document chunking strategies."""

    @abstractmethod
    def chunk(self, text: str) -> list[str]:
        """Split the document into chunks.

        Args:
            text (str): The text to be chunked.

        Returns:
            list[str]: A list of text chunks.
        """
        pass
