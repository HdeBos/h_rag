"""Module containing the LLM class for interacting with the Ollama API."""

from typing import override

from loguru import logger
from mistralai.client import Mistral

from h_rag.llm.llm import LLM


class MistralWrapper(LLM):
    """Class for interacting with Mistral models."""

    def __init__(self):
        self.client = Mistral()
        self.chat_history = []

    @override
    def health_check(self) -> bool:
        try:
            self.client.models.list()
            logger.info("Mistral health check successful")
            return True
        except Exception as e:
            logger.error(f"Mistral health check failed: {e}")
            return False

    @override
    def get_models(self) -> list[str]:
        models = self.client.models.list()
        return [model.id for model in models.data]

    @override
    def query(self, model: str, prompt: str) -> str:
        response = self.client.chat.complete(
            model=model,
            messages=self.chat_history + [{"role": "user", "content": prompt}],
            response_format={
                "type": "text",
            },
        )
        self.chat_history += [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response.choices[0].message.content},
        ]
        return response.choices[0].message.content


if __name__ == "__main__":
    llm = MistralWrapper()
    response = llm.health_check()
