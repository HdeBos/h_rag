"""Knowledge Base API router for handling knowledge base-related endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from h_rag.api.dependencies import get_knowledge_bases_service
from h_rag.models.file_data import FileData
from h_rag.services.knowledge_bases import KnowledgeBasesService

router = APIRouter(
    prefix="/knowledge-bases",
    tags=["Knowledge bases"],
)


@router.get("/")
def get_knowledge_bases(
    service: Annotated[KnowledgeBasesService, Depends(get_knowledge_bases_service)],
) -> list[str]:
    """Get all available knowledge bases.

    Args:
        service: The KnowledgeBasesService instance.

    Returns:
        A list of knowledge base names.
    """
    return service.get_knowledge_bases()


@router.delete("/{knowledge_base_name}", status_code=204)
def delete_knowledge_base(
    service: Annotated[KnowledgeBasesService, Depends(get_knowledge_bases_service)],
    knowledge_base_name: str,
) -> None:
    """Delete a knowledge base.

    Args:
        service: The KnowledgeBasesService instance injected by FastAPI.
        knowledge_base_name: The name of the knowledge base to delete.
    """
    service.delete_knowledge_base(knowledge_base_name)


@router.post("/", status_code=201)
def create_knowledge_base(
    service: Annotated[KnowledgeBasesService, Depends(get_knowledge_bases_service)],
    file_data: FileData,
) -> str:
    """Create a knowledge base.

    Args:
        service: The KnowledgeBasesService instance injected by FastAPI.
        file_data: The data of the file to be processed and added to the knowledge base.

    Returns:
        The result of the knowledge base creation operation.
    """
    return service.create_knowledge_base(file_data)


@router.post("/{knowledge_base_name}/documents", status_code=201)
def add_document_to_knowledge_base(
    service: Annotated[KnowledgeBasesService, Depends(get_knowledge_bases_service)],
    knowledge_base_name: str,
    file_name: str,
) -> str:
    """Add a document to an existing knowledge base.

    Args:
        service: The KnowledgeBasesService instance injected by FastAPI.
        knowledge_base_name: The name of the knowledge base to add the document to.
        file_name: The name of the document to be added.

    Returns:
        The result of the document addition operation.
    """
    return service.add_document_to_knowledge_base(knowledge_base_name, file_name)


@router.delete("/{knowledge_base_name}/files/{file_name}", status_code=204)
def remove_document_from_knowledge_base(
    service: Annotated[KnowledgeBasesService, Depends(get_knowledge_bases_service)],
    knowledge_base_name: str,
    file_name: str,
) -> None:
    """Remove a document from an existing knowledge base.

    Args:
        service: The KnowledgeBasesService instance injected by FastAPI.
        knowledge_base_name: The name of the knowledge base to remove the document from.
        file_name: The name of the document to be removed.
    """
    service.remove_document_from_knowledge_base(knowledge_base_name, file_name)
