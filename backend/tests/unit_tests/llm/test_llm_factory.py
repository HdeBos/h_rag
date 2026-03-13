"""Unit tests for the LLMFactory class."""

import pytest

from h_rag.llm.gemini_wrapper import GeminiWrapper
from h_rag.llm.llm_factory import LLMFactory
from h_rag.llm.ollama_wrapper import OllamaWrapper


class TestLLMFactory:
    """Test suite for the LLMFactory class."""

    @pytest.fixture()
    def mock_config_wrapper(self, mock_config):
        """Fixture that wraps mock_config so only return_value is required."""

        def _wrapper(return_value: str) -> None:
            mock_config("h_rag.llm.llm_factory", "llm", "provider", return_value=return_value)

        return _wrapper

    def test_get_llm_gemini(self, mock_config_wrapper) -> None:
        """Test that the factory returns a GeminiWrapper for provider 'Gemini'."""
        mock_config_wrapper("Gemini")
        llm = LLMFactory.get_llm()
        assert isinstance(llm, GeminiWrapper)

    def test_get_llm_ollama(self, mock_config_wrapper) -> None:
        """Test that the factory returns an OllamaWrapper for provider 'Ollama'."""
        mock_config_wrapper("Ollama")
        llm = LLMFactory.get_llm()
        assert isinstance(llm, OllamaWrapper)

    def test_get_llm_unknown_provider_raises_error(self, mock_config_wrapper) -> None:
        """Test that requesting an unknown provider raises ValueError."""
        mock_config_wrapper("Unknown")
        with pytest.raises(ValueError) as exc:
            LLMFactory.get_llm()
        assert "Unknown LLM provider" in str(exc.value)
