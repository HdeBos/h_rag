"""Module for the LLM Factory."""

from h_rag.config.config_wrapper import get_config
from h_rag.llm.gemini_wrapper import GeminiWrapper
from h_rag.llm.llm import LLM
from h_rag.llm.ollama_wrapper import OllamaWrapper


class LLMFactory:
    """Factory class for creating LLM instances based on the provider."""

    _llm_providers = {
        "Gemini": GeminiWrapper,
        "Ollama": OllamaWrapper,
    }

    @classmethod
    def get_llm(cls) -> LLM:
        """Factory Method."""
        provider = get_config("llm", "provider")
        try:
            return cls._llm_providers[provider]()
        except KeyError:
            raise ValueError(
                f"Unknown LLM provider: {provider}, available providers: {list(cls._llm_providers.keys())}"
            )
