"""Chat API router for handling chat-related endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from h_rag.models.chat_query import ChatQuery
from h_rag.services.chat import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/models")
def get_models(service: Annotated[ChatService, Depends(ChatService)]) -> list[str]:
    """Endpoint to get available models.

    Args:
        service: The ChatService instance injected by FastAPI.

    Returns:
        A list of available models from the LLM.
    """
    return service.get_models()


@router.post("/query")
def query(
    service: Annotated[ChatService, Depends(ChatService)],
    chat_query: ChatQuery,
) -> str:
    """Endpoint to handle chat queries.

    Args:
        service: The ChatService instance injected by FastAPI.
        chat_query: The chat query input from the user.

    Returns:
        The response from the LLM.
    """
    return service.query(chat_query.query, chat_query.model, chat_query.knowledge_base)
