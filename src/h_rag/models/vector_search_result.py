"""Model for the result of a query to a vector database."""

from pydantic import BaseModel, Field


class VectorSearchResult(BaseModel):
    """Class for vector database query result."""

    id: str = Field(description="Unique identifier for the retrieved chunk")
    chunk: str = Field(description="The chunk of text that was retrieved from the vector database")
    similarity: float = Field(
        description="The similarity score of the retrieved chunk to the query"
    )
