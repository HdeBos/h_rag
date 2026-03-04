"""Service layer for the chat router."""

from h_rag.llm.llm_factory import LLMFactory


class ChatService:
    """Service for handling chat interactions."""

    def get_models(self):
        """Get available models."""
        llm = LLMFactory.get_llm()
        return llm.get_models()
