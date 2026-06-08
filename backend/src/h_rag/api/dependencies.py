"""FastAPI dependency providers for shared application resources."""

from typing import Annotated

from fastapi import Depends, Request

from h_rag.db.postgres_wrapper import PostgresWrapper
from h_rag.services.chat import ChatService
from h_rag.services.knowledge_bases import KnowledgeBasesService


def get_postgres_wrapper(request: Request):
    """Provide the shared PostgresWrapper from app state."""
    return request.app.state.postgres_wrapper


def get_knowledge_bases_service(
    postgres_wrapper: Annotated[PostgresWrapper, Depends(get_postgres_wrapper)],
) -> KnowledgeBasesService:
    """Provide a KnowledgeBasesService backed by the shared connection pool."""
    return KnowledgeBasesService(postgres_wrapper)


def get_chat_service(
    postgres_wrapper: Annotated[PostgresWrapper, Depends(get_postgres_wrapper)],
) -> ChatService:
    """Provide a ChatService backed by the shared connection pool."""
    return ChatService(postgres_wrapper)
