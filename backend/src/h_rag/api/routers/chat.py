"""Chat API router for handling chat-related endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from h_rag.api.dependencies import get_chat_service
from h_rag.models.chat_query import ChatQuery
from h_rag.models.chat_response import ChatResponse
from h_rag.services.chat import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.get("/models")
def get_models(service: Annotated[ChatService, Depends(get_chat_service)]) -> list[str]:
    """Get available LLM models.

    Args:
        service: The ChatService instance injected by FastAPI.

    Returns:
        A list of available models from the LLM.
    """
    return service.get_models()


@router.post("/query", status_code=200)
def query(
    service: Annotated[ChatService, Depends(get_chat_service)],
    chat_query: ChatQuery,
) -> ChatResponse:
    """Handle a chat query and return a response.

    Args:
        service: The ChatService instance injected by FastAPI.
        chat_query: The chat query input from the user.

    Returns:
        The response from the LLM.
    """
    return service.query(chat_query)
