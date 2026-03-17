"""Wrapper for Chroma vector database."""

from typing import override

import chromadb
from loguru import logger

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
    def insert(
        self,
        name: str,
        chunks: list[str],
        doc_name: str,
        pages: list[int],
    ) -> None:
        collection = self.client.get_collection(name)
        ids = [str(i) for i in range(len(chunks))]
        metadata = [{"document_name": doc_name, "page": page} for page in pages]
        embeddings = [self.encode(chunk, "document") for chunk in chunks]
        collection.add(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadata)  # type: ignore

    def _process_query_result(self, chunk_id, chunk, meta) -> VectorSearchResult:
        """Process a single query result from Chroma into a VectorSearchResult object."""
        document = str(meta.get("document_name", "unknown_document"))
        page = meta.get("page")
        if not isinstance(page, int):
            logger.warning(
                f"Expected page number to be an int, but got {type(page)}. Defaulting to 0."
            )
            page = 0
        return VectorSearchResult(id=chunk_id, chunk=chunk, document=document, page=page)

    def _process_query_results(self, results: chromadb.QueryResult) -> list[VectorSearchResult]:
        """Process the raw results returned by Chroma into a list of VectorSearchResult objects."""
        documents = results.get("documents")
        metadatas = results.get("metadatas")
        ids = results.get("ids")

        if documents is None or metadatas is None:
            raise ValueError("Chroma query returned incomplete results")

        return [
            self._process_query_result(chunk_id, chunk, meta)
            for chunk_id, chunk, meta in zip(ids[0], documents[0], metadatas[0])
        ]

    @override
    def query(self, name: str, query: str, n_results: int = 5) -> list[VectorSearchResult]:
        collection = self.client.get_collection(name)
        query_embedding = self.encode(query, "query")
        results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
        vector_search_results = self._process_query_results(results)
        return vector_search_results
