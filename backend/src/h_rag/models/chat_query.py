"""Pydantic model for chat query input."""

from pydantic import BaseModel, Field


class ChatQuery(BaseModel):
    """Pydantic model for chat query input."""

    query: str = Field(description="The user's chat query.")
    model: str = Field(description="The model to use for the query.")
    knowledge_base: str = Field(description="The knowledge base to use for the query.")
