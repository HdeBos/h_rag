"""Wrapper for Chroma vector database."""

from typing import override

import chromadb
import numpy as np

from h_rag.models.vector_search_result import VectorSearchResult
from h_rag.vector_db.vector_db import VectorDB


class ChromaWrapper(VectorDB):
    """Wrapper for Chroma vector database."""

    def __init__(self):
        """Initialize the Chroma client."""
        super().__init__()
        self.client = chromadb.PersistentClient(".chroma")

    @override
    def create(self, name: str) -> None:
        self.client.create_collection(name)

    @override
    def delete(self, name: str) -> None:
        self.client.delete_collection(name)

    @override
    def get_knowledge_bases(self) -> list[str]:
        collections = self.client.list_collections()
        return [collection.name for collection in collections]

    @override
    def insert(self, name: str, chunks: list[str]) -> None:
        collection = self.client.get_collection(name)
        ids = [str(i) for i in range(len(chunks))]
        collection.add(ids=ids, documents=chunks)

    @override
    def query(self, name: str, query: str, n_results: int = 5) -> list[VectorSearchResult]:
        collection = self.client.get_collection(name)
        results = collection.query(query_texts=[query], n_results=n_results)
        if results["documents"] is None or results["distances"] is None:
            raise ValueError("Chroma query returned incomplete results")
        vector_search_results = [
            VectorSearchResult(id=id, chunk=chunk, similarity=similarity)
            for (id, chunk, similarity) in zip(
                results["ids"][0], results["documents"][0], results["distances"][0]
            )
        ]
        return vector_search_results

    @override
    def encode(self, text: str | list[str], type: str | None = None) -> np.ndarray:
        if type:
            text = (
                f"search_{type}:" + text
                if isinstance(text, str)
                else [f"search_{type}:" + t for t in text]
            )
        embeddings = self.embedding_model.encode(text)
        return np.asarray(embeddings, dtype=float)

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
