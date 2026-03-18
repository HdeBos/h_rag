"""Shared fixtures for all tests."""

import pytest
from pytest_mock import MockerFixture


@pytest.fixture()
def mock_embedding_init(mocker: MockerFixture):
    """Fixture to mock the Embedding.__init__ method to avoid loading embedding model."""
    mocker.patch(
        "h_rag.data_processing.embedding.Embedding.__init__", return_value=None, autospec=True
    )
