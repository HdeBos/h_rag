"""Knowledge Base API router for handling knowledge base-related endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from h_rag.services.knowledge_bases import KnowledgeBasesService

router = APIRouter(
    prefix="/knowledge-bases",
    tags=["knowledge-bases"],
)


@router.get("/")
def get_knowledge_bases(
    service: Annotated[KnowledgeBasesService, Depends(KnowledgeBasesService)],
):
    """Endpoint to get available knowledge bases."""
    return service.get_knowledge_bases()


@router.delete("/{knowledge_base_name}")
def delete_knowledge_base(
    service: Annotated[KnowledgeBasesService, Depends(KnowledgeBasesService)],
    knowledge_base_name: str,
):
    """Endpoint to delete a knowledge base."""
    return service.delete_knowledge_base(knowledge_base_name)
