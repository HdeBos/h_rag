"""Unit tests for the LLMFactory class."""

import pytest

from h_rag.llm.gemini_wrapper import GeminiWrapper
from h_rag.llm.llm_factory import LLMFactory
from h_rag.llm.ollama_wrapper import OllamaWrapper


class TestLLMFactory:
    """Test suite for the LLMFactory class."""

    @staticmethod
    def test_get_llm_gemini():
        """Test that the factory returns a GeminiWrapper for provider 'Gemini'."""
        llm = LLMFactory.get_llm("Gemini")
        assert isinstance(llm, GeminiWrapper)

    @staticmethod
    def test_get_llm_ollama():
        """Test that the factory returns an OllamaWrapper for provider 'Ollama'."""
        llm = LLMFactory.get_llm("Ollama")
        assert isinstance(llm, OllamaWrapper)

    @staticmethod
    def test_get_llm_unknown_provider_raises_error():
        """Test that requesting an unknown provider raises ValueError."""
        with pytest.raises(ValueError) as exc:
            LLMFactory.get_llm("Unknown")
        assert "Unknown LLM provider" in str(exc.value)
