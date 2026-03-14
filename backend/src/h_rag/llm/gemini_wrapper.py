"""Gemini API implemention of the LLM class."""

from typing import override

from google import genai
from loguru import logger

from h_rag.llm.llm import LLM


class GeminiWrapper(LLM):
    """Class for interacting with the Gemini model from Google."""

    def __init__(self):
        """Initialize the LLM class."""
        self.chat_history = []

    @override
    def health_check(self) -> bool:
        try:
            client = genai.Client()
            client.models.list()
            logger.info("Gemini health check successful")
            return True
        except Exception as e:
            logger.error(f"Gemini health check failed: {e}")
            return False

    @override
    def get_models(self) -> list[str]:
        client = genai.Client()
        model_info = client.models.list()
        models = [
            model.name.replace("models/", "") for model in model_info if model.name is not None
        ]
        return models

    @override
    def query(self, model: str, prompt: str) -> str:
        logger.debug(f"Querying {model} with question: {prompt}")
        client = genai.Client()
        response = client.models.generate_content(
            model=model,
            contents=self.chat_history + [{"role": "user", "parts": [{"text": prompt}]}],
        )
        self.chat_history += [
            {"role": "user", "parts": [{"text": prompt}]},
            {"role": "model", "parts": [{"text": response.text}]},
        ]
        if not isinstance(response.text, str):
            raise ValueError("Querying Gemini failed")
        return response.text
