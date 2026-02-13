"""Unit tests for the LLM class."""

import pytest
from pytest_mock import MockerFixture

from h_rag.llm.ollama_wrapper import OllamaWrapper


class TestOllamaWrapper:
    """Test suite for the OllamaWrapper class."""

    @pytest.fixture()
    def mock_ollama_chat(self, mocker: MockerFixture) -> MockerFixture:
        """Fixture to mock the ollama.chat function."""
        return mocker.patch(
            "h_rag.llm.ollama_wrapper.ollama.chat", return_value={"message": {"content": "Paris"}}
        )

    def test_query_extends_history(self, mock_ollama_chat: MockerFixture) -> None:
        """Test that the query method extends the chat history."""
        # Arrange
        llm = OllamaWrapper()
        response = llm.query("mock_model", "What is the capital of Germany?")
        initial_chat_history_length = len(llm.chat_history)

        # Act
        response = llm.query("mock_model", "What is the capital of France?")

        # Assert
        assert response == "Paris"
        assert len(llm.chat_history) == initial_chat_history_length + 2
        assert llm.chat_history[-2]["role"] == "user"
        assert llm.chat_history[-2]["content"] == "What is the capital of France?"
        assert llm.chat_history[-1]["role"] == "assistant"
        assert llm.chat_history[-1]["content"] == response
