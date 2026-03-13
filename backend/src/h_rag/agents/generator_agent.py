"""GeneratorAgent implementation."""

from string import Template

from h_rag.llm.llm_factory import LLMFactory
from h_rag.prompts.generator_prompts import generate_response_prompt


class GeneratorAgent:
    """Agent responsible for generating responses based on retrieved information."""

    def __init__(self, model: str):
        """Initialize the GeneratorAgent."""
        self.llm = LLMFactory.get_llm()
        self.model = model

    def generate(self, query: str, chunks: list[str]) -> str:
        """Generate a response based on the query and retrieved information.

        Args:
            query (str): The original query.
            chunks (list[str]): A list of relevant information retrieved from the vector database.

        Returns:
            str: The generated response.
        """
        prompt = Template(generate_response_prompt).substitute(
            query=query,
            chunks=chunks,
        )
        response = self.llm.query(self.model, prompt)
        return response
