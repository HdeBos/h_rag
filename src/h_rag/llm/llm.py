"""Module containing the LLM class for interacting with the Ollama API."""

from abc import ABC, abstractmethod


class LLM(ABC):
    """Abstract base class for interacting with LLMs."""

    @abstractmethod
    def get_models(self) -> list[str]:
        """Get a list of available models.

        Returns:
            list[str]: A list of available models.
        """
        pass

    @abstractmethod
    def query(self, model: str, prompt: str) -> str:
        """Query the llm.

        Args:
            model (str): The model to query.
            prompt (str): The prompt to ask the model.

        Returns:
            str: The response from the model.
        """
        pass
