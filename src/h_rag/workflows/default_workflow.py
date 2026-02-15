"""Default workflow implementation."""

from typing import override

from h_rag.agents.generator_agent import GeneratorAgent
from h_rag.agents.retriever_agent import RetrieverAgent
from h_rag.workflows.workflow import Workflow


class DefaultWorkflow(Workflow):
    """Default workflow implementation."""

    def __init__(self, model: str, knowledge_base: str):
        """Initialize the DefaultWorkflow."""
        self.retriever_agent = RetrieverAgent(knowledge_base)
        self.generator_agent = GeneratorAgent(model)

    @override
    def execute(self, query: str) -> str:
        """Execute the workflow on the given query.

        Args:
            query (str): The query to be processed.

        Returns:
            str: The result of the workflow execution.
        """
        records = self.retriever_agent.retrieve(query)
        chunks = self.retriever_agent.get_chunks(records)
        response = self.generator_agent.generate(query, chunks)
        return response
