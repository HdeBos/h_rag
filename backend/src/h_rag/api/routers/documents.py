"""Knowledge Base API router for handling knowledge base-related endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from h_rag.api.dependencies import get_documents_service
from h_rag.services.documents import DocumentsService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/")
def list_files(
    service: Annotated[DocumentsService, Depends(get_documents_service)],
) -> list[str]:
    """List all files in the knowledge base.

    Args:
        service: The DocumentsService instance injected by FastAPI.

    Returns:
        A list of file names available in the knowledge base.
    """
    return service.list_files()


@router.get("/{file_name}")
def get_file(
    service: Annotated[DocumentsService, Depends(get_documents_service)],
    file_name: str,
) -> str:
    """Retrieve a file from the knowledge base.

    Args:
        service: The DocumentsService instance injected by FastAPI.
        file_name: The name of the file to retrieve.

    Returns:
        The base64-encoded string of the requested file.
    """
    return service.get_file(file_name)


@router.get("/{file_name}/highlighted")
def get_highlighted_file(
    service: Annotated[DocumentsService, Depends(get_documents_service)],
    file_name: str,
    highlight: str,
) -> str:
    """Get highlighted content from a file.

    Args:
        service: The DocumentsService instance injected by FastAPI.
        file_name: The name of the file to retrieve.
        highlight: The text to highlight in the file.

    Returns:
        The highlighted content from the file.
    """
    return service.get_highlighted_file(file_name, highlight)
