"""Unit tests for the LLMFactory class."""

import pytest
from pytest_mock import MockerFixture

from h_rag.llm.gemini_wrapper import GeminiWrapper
from h_rag.llm.llm_factory import LLMFactory
from h_rag.llm.ollama_wrapper import OllamaWrapper


class TestLLMFactory:
    """Test suite for the LLMFactory class."""

    @pytest.fixture()
    def mock_config(self, mocker: MockerFixture):
        """Fixture to mock the get_config function with a dynamic return value."""

        def _mock(return_value: str):
            return mocker.patch(
                "h_rag.llm.llm_factory.get_config",
                return_value=return_value,
            )

        return _mock

    def test_get_llm_gemini(self, mock_config) -> None:
        """Test that the factory returns a GeminiWrapper for provider 'Gemini'."""
        mock_config("Gemini")
        llm = LLMFactory.get_llm()
        assert isinstance(llm, GeminiWrapper)

    def test_get_llm_ollama(self, mock_config) -> None:
        """Test that the factory returns an OllamaWrapper for provider 'Ollama'."""
        mock_config("Ollama")
        llm = LLMFactory.get_llm()
        assert isinstance(llm, OllamaWrapper)

    def test_get_llm_unknown_provider_raises_error(self, mock_config) -> None:
        """Test that requesting an unknown provider raises ValueError."""
        mock_config("Unknown")
        with pytest.raises(ValueError) as exc:
            LLMFactory.get_llm()
        assert "Unknown LLM provider" in str(exc.value)
