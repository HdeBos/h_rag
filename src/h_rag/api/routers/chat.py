"""Chat API router for handling chat-related endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from h_rag.services.chat import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/models")
def get_models(service: Annotated[ChatService, Depends(ChatService)]):
    """Endpoint to get available models."""
    return service.get_models()
