"""Knowledge Base API router for handling knowledge base-related endpoints."""

import base64
from typing import Annotated

from fastapi import APIRouter, Depends

from h_rag.models.file_data import FileData
from h_rag.services.knowledge_bases import KnowledgeBasesService

router = APIRouter(
    prefix="/knowledge-bases",
    tags=["knowledge-bases"],
)


@router.get("/")
def get_knowledge_bases(
    service: Annotated[KnowledgeBasesService, Depends(KnowledgeBasesService)],
) -> list[str]:
    """Endpoint to get available knowledge bases."""
    return service.get_knowledge_bases()


@router.delete("/{knowledge_base_name}")
def delete_knowledge_base(
    service: Annotated[KnowledgeBasesService, Depends(KnowledgeBasesService)],
    knowledge_base_name: str,
):
    """Endpoint to delete a knowledge base."""
    return service.delete_knowledge_base(knowledge_base_name)


@router.post("/")
def create_knowledge_base(
    service: Annotated[KnowledgeBasesService, Depends(KnowledgeBasesService)],
    file_data: FileData,
):
    """Endpoint to create a knowledge base.

    Args:
        service: The KnowledgeBasesService instance injected by FastAPI.
        file_data: The data of the file to be processed and added to the knowledge base.

    Returns:
        The result of the knowledge base creation operation.
    """
    file_data.data = base64.b64decode(file_data.data)
    return service.create_knowledge_base(file_data)
