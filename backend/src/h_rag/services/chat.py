"""Service layer for the chat router."""

from h_rag.llm.llm_factory import LLMFactory
from h_rag.workflows.workflow_factory import WorkflowFactory


class ChatService:
    """Service for handling chat interactions."""

    def get_models(self) -> list[str]:
        """Get available models.

        Returns:
            A list of available models from the LLM.
        """
        llm = LLMFactory.get_llm()
        return llm.get_models()

    def query(self, query: str, model: str, knowledge_base: str) -> str:
        """Handle a chat query.

        Args:
            query: The user's chat query.
            model: The model to use for the query.
            knowledge_base: The knowledge base to use for the query.

        Returns:
            The response from the LLM.
        """
        workflow = WorkflowFactory.get_workflow(model, knowledge_base)
        response = workflow.execute(query)
        return response
