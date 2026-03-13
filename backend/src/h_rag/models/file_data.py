"""Module for file data models."""

from pydantic import BaseModel, Field


class FileData(BaseModel):
    """Class for file data."""

    name: str = Field(description="The name of the file.")
    data: bytes | str = Field(description="The raw data of the file.")
    type: str = Field(description="The type of the file.")
