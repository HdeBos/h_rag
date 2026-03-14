"""Module for document data models."""

from pydantic import BaseModel, Field


class DocumentData(BaseModel):
    """Class for document data."""

    # file_id: str = Field(description="Unique identifier for the file")
    data: bytes = Field(description="Binary data of the file")
    name: str = Field(description="Name of the file")
    type: str = Field(description="Type of the file")
    chunks: list[str] = Field(description="Extracted text chunks from the file")
    chunk_pages: list[int] = Field(description="1-based page number for each chunk")
