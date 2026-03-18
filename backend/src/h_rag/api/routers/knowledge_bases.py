"""Knowledge Base API router for handling knowledge base-related endpoints."""

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
) -> str:
    """Endpoint to delete a knowledge base."""
    return service.delete_knowledge_base(knowledge_base_name)


@router.post("/")
def create_knowledge_base(
    service: Annotated[KnowledgeBasesService, Depends(KnowledgeBasesService)],
    file_data: FileData,
) -> str:
    """Endpoint to create a knowledge base.

    Args:
        service: The KnowledgeBasesService instance injected by FastAPI.
        file_data: The data of the file to be processed and added to the knowledge base.

    Returns:
        The result of the knowledge base creation operation.
    """
    return service.create_knowledge_base(file_data)


@router.get("/files/{file_name}")
def get_file(
    service: Annotated[KnowledgeBasesService, Depends(KnowledgeBasesService)],
    file_name: str,
) -> str:
    """Endpoint to retrieve a file from the knowledge base.

    Args:
        service: The KnowledgeBasesService instance injected by FastAPI.
        file_name: The name of the file to retrieve.

    Returns:
        The base64-encoded string of the requested file.
    """
    return service.get_file(file_name)


@router.get("/files/{file_name}/{highlight}")
def get_highlighted_file(
    service: Annotated[KnowledgeBasesService, Depends(KnowledgeBasesService)],
    file_name: str,
    highlight: str,
) -> str:
    """Endpoint to get highlighted content from a file.

    Args:
        service: The KnowledgeBasesService instance injected by FastAPI.
        file_name: The name of the file to retrieve.
        highlight: The text to highlight in the file.

    Returns:
        The highlighted content from the file.
    """
    return service.get_highlighted_file(file_name, highlight)
