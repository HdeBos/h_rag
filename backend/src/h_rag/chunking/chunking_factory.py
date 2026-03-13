"""Module for the Chunking Factory."""

from h_rag.chunking.chunking import Chunking
from h_rag.chunking.fixed_size_chunking import FixedSizeChunking
from h_rag.chunking.semantic_chunking import SemanticChunking
from h_rag.config.config_wrapper import get_config


class ChunkingFactory:
    """Factory class for creating Chunking instances based on the provider."""

    _chunking_methods = {
        "FixedSize": FixedSizeChunking,
        "Semantic": SemanticChunking,
        # POSSIBLE FUTURE METHODS:
        # Recursive / Hierarchical Chunking
        # Contextual / Query-Aware Chunking (Dynamic Chunking)
        # Graph-Based / Knowledge-Aware Chunking
    }

    @classmethod
    def get_chunking_method(cls) -> Chunking:
        """Factory Method."""
        method = get_config("chunking", "method")
        try:
            return cls._chunking_methods[method]()
        except KeyError:
            raise ValueError(
                f"Unknown chunking method: {method}, available methods: {list(cls._chunking_methods.keys())}"
            )
