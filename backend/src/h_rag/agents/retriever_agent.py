"""Module for the RetrieverAgent."""

from loguru import logger

from h_rag.models.vector_search_result import VectorSearchResult
from h_rag.vector_db.vector_db_factory import VectorDBFactory


class RetrieverAgent:
    """Agent responsible for retrieving relevant information from the vector database."""

    def __init__(self, knowledge_base: str):
        """Initialize the RetrieverAgent with a vector database instance."""
        self.vector_db = VectorDBFactory.get_vector_db()
        self.knowledge_base = knowledge_base

    def get_chunks(self, results: list[VectorSearchResult]) -> list[str]:
        """Extract text chunks from the search results.

        Args:
            results (list[VectorSearchResult]): The search results from the vector database.

        Returns:
            list[str]: A list of relevant text chunks retrieved from the vector database.
        """
        return [result.chunk for result in results]

    def retrieve(self, query: str) -> list[VectorSearchResult]:
        """Retrieve relevant information from the vector database based on the query.

        Args:
            query (str): The query to retrieve information for.

        Returns:
            list[VectorSearchResult]: A list of relevant information retrieved from the vector database.
        """
        records = self.vector_db.query(self.knowledge_base, query)
        logger.info(f"Retrieved {len(records)} records from knowledge base'")
        logger.debug(f"Retrieved records: {records}")
        return records
