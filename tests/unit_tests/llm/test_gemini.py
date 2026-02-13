"""Unit tests for the LLM class."""

import pytest
from pytest_mock import MockerFixture

from h_rag.llm.gemini_wrapper import GeminiWrapper


class TestGeminiWrapper:
    """Test suite for the GeminiWrapper class."""

    @pytest.fixture()
    def mock_gemini_chat(self, mocker: MockerFixture) -> MockerFixture:
        """Fixture to mock the gemini generate_content function."""
        mock_client = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.text = "Paris"
        mock_client.models.generate_content.return_value = mock_response
        return mocker.patch("h_rag.llm.gemini_wrapper.genai.Client", return_value=mock_client)

    def test_query_extends_history(self, mock_gemini_chat: MockerFixture) -> None:
        """Test that the query method extends the chat history."""
        # Arrange
        llm = GeminiWrapper()
        response = llm.query("mock_model", "What is the capital of Germany?")
        initial_chat_history_length = len(llm.chat_history)

        # Act
        response = llm.query("mock_model", "What is the capital of France?")

        # Assert
        assert response == "Paris"
        assert len(llm.chat_history) == initial_chat_history_length + 2
        assert llm.chat_history[-2]["role"] == "user"
        assert llm.chat_history[-2]["parts"][0]["text"] == "What is the capital of France?"
        assert llm.chat_history[-1]["role"] == "model"
        assert llm.chat_history[-1]["parts"][0]["text"] == response
