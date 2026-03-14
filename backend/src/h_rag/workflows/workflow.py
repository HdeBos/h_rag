"""ABC for workflows for retrieval-augmented generation (RAG) system."""

from abc import ABC, abstractmethod

from h_rag.models.chat_response import ChatResponse


class Workflow(ABC):
    """Base class for workflows."""

    @abstractmethod
    def execute(self, query: str) -> ChatResponse:
        """Execute the workflow on the given query.

        Args:
            query (str): The query to be processed.

        Returns:
            ChatResponse: The result of the workflow execution.
        """
        pass
