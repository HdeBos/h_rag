"""Unit tests for the LLM class."""

import pytest
from pytest_mock import MockerFixture

from h_rag.llm.mistral_wrapper import MistralWrapper


class TestMistralWrapper:
    """Test suite for the MistralWrapper class."""

    @pytest.fixture()
    def mock_mistral_chat(self, mocker: MockerFixture) -> MockerFixture:
        """Fixture to mock the mistral chat.complete function."""
        mock_client = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_choice = mocker.MagicMock()
        mock_message = mocker.MagicMock()
        mock_message.content = "Paris"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.complete.return_value = mock_response
        return mocker.patch("h_rag.llm.mistral_wrapper.Mistral", return_value=mock_client)

    def test_query_extends_history(self, mock_mistral_chat: MockerFixture) -> None:
        """Test that the query method extends the chat history."""
        # Arrange
        llm = MistralWrapper()
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