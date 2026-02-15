"""ABC for workflows for retrieval-augmented generation (RAG) system."""

from abc import ABC, abstractmethod


class Workflow(ABC):
    """Base class for workflows."""

    @abstractmethod
    def execute(self, query: str) -> str:
        """Execute the workflow on the given query.

        Args:
            query (str): The query to be processed.

        Returns:
            str: The result of the workflow execution.
        """
        pass
