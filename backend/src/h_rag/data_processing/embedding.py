"""ABC for document chunking strategies for retrieval-augmented generation (RAG) systems."""

from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from h_rag.config.config_wrapper import get_config


@lru_cache(maxsize=1)
def _load_embedding_model(model_name: str, revision: str) -> SentenceTransformer:
    return SentenceTransformer(model_name, trust_remote_code=True, revision=revision)


class Embedding:
    """Base class for document chunking strategies."""

    def __init__(self) -> None:
        """Initialize the vector database."""
        model_name = get_config("vector_db", "embedding_model", "name")
        revision = get_config("vector_db", "embedding_model", "revision")
        self.embedding_model = _load_embedding_model(model_name, revision)

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
