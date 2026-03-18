"""Module for the RetrieverAgent."""

from loguru import logger

from h_rag.db.vector_db.vector_db_factory import VectorDbFactory
from h_rag.models.vector_search_result import VectorSearchResult


class RetrieverAgent:
    """Agent responsible for retrieving relevant information from the vector database."""

    def __init__(self, knowledge_base: str):
        """Initialize the RetrieverAgent with a vector database instance."""
        self.vector_db = VectorDbFactory.get_vector_db()
        self.knowledge_base = knowledge_base

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
