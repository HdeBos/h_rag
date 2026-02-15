"""Module for Fixed Size Chunking."""

from typing import override

from h_rag.chunking.chunking import Chunking
from h_rag.config.config_wrapper import get_config


class FixedSizeChunking(Chunking):
    """Chunking strategy that splits documents into fixed-size chunks."""

    def _get_chunk_size(self) -> int:
        """Get the chunk size from the configuration.

        Returns:
            int: The number of characters in each chunk.
        """
        return int(get_config("chunking", "size"))

    def _get_overlap(self) -> int:
        """Get the overlap size from the configuration.

        Returns:
            int: The number of characters to overlap between chunks.
        """
        return int(get_config("chunking", "overlap"))

    @override
    def chunk(self, text: str) -> list[str]:
        complete_text = text
        chunk_size = self._get_chunk_size()
        overlap = self._get_overlap()

        chunks: list[str] = []
        for i in range(0, len(complete_text), chunk_size - overlap):
            chunks.append(complete_text[i : i + chunk_size])
        return chunks
