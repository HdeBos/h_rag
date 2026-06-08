"""Service layer for the chat router."""

from h_rag.db.postgres_wrapper import PostgresWrapper
from h_rag.llm.llm_factory import LLMFactory
from h_rag.models.chat_response import ChatResponse
from h_rag.workflows.workflow_factory import WorkflowFactory
from src.h_rag.models.chat_query import ChatQuery


class ChatService:
    """Service for handling chat interactions."""

    def __init__(self, pg_conn: PostgresWrapper):
        """Initialize the knowledge bases service."""
        self._pg = pg_conn

    def get_models(self) -> list[str]:
        """Get available models.

        Returns:
            A list of available models from the LLM.
        """
        llm = LLMFactory.get_llm()
        return llm.get_models()

    def query(self, chat_query: ChatQuery) -> ChatResponse:
        """Handle a chat query.

        Args:
            chat_query: The chat query input from the user.

        Returns:
            The response from the LLM.
        """
        workflow = WorkflowFactory.get_workflow(
            self._pg, chat_query.model, chat_query.knowledge_base
        )
        response = workflow.execute(chat_query.query)
        return response
