"""GeneratorAgent implementation."""

import json

from loguru import logger

from h_rag.llm.llm_factory import LLMFactory
from h_rag.models.chat_response import ChatResponse
from h_rag.models.vector_search_result import VectorSearchResult
from h_rag.prompts.generator_prompts import generate_response_prompt


class GeneratorAgent:
    """Agent responsible for generating responses based on retrieved information."""

    def __init__(self, model: str):
        """Initialize the GeneratorAgent."""
        self.llm = LLMFactory.get_llm()
        self.model = model

    def generate(self, query: str, chunks: list[VectorSearchResult]) -> ChatResponse:
        """Generate a response based on the query and retrieved information.

        Args:
            query (str): The original query.
            chunks (list[VectorSearchResult]): A list of relevant information retrieved from the vector database.

        Returns:
            ChatResponse: The generated response along with the associated chunk and document.
        """
        prompt = generate_response_prompt.format(
            query=query,
            chunks=[chunk.model_dump_json() for chunk in chunks],
        )
        response = self.llm.query(self.model, prompt)
        logger.info(f"LLM response: {response}")
        response_json = json.loads(response)
        id = response_json.get("chunk")
        chunk = next((chunk for chunk in chunks if chunk.id == id), None)
        if chunk is None:
            logger.info(f"Chunk with id {id} not found in retrieved chunks")
            chunk = VectorSearchResult(id=id, chunk="", document="", page=0)
        return ChatResponse(
            response=response_json.get("response"),
            chunk=chunk.chunk,
            document=chunk.document,
            page=chunk.page,
        )
