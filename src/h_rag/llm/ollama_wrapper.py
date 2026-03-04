"""Module containing the LLM class for interacting with the Ollama API."""

from typing import override

import ollama
from loguru import logger

from h_rag.llm.llm import LLM


class OllamaWrapper(LLM):
    """Class for interacting with the Ollama models."""

    def __init__(self):
        """Initialize the LLM class."""
        self.chat_history: list[dict[str, str]] = []

    @override
    def health_check(self) -> bool:
        try:
            ollama.list()
            return True
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False

    @override
    def get_models(self) -> list[str]:
        client = ollama.Client()
        models_info = client.list()
        models = [model["model"] for model in models_info.get("models", [])]
        return models

    @override
    def query(self, model: str, prompt: str) -> str:
        logger.info(f"Querying {model} with question: {prompt}")
        response = ollama.chat(
            model=model,
            messages=self.chat_history + [{"role": "user", "content": prompt}],
        )
        self.chat_history += [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response["message"]["content"]},
        ]

        return response["message"]["content"]
