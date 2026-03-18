"""Integration tests for PgVectorWrapper."""

import pytest
from pytest_mock import MockerFixture

from h_rag.config.config_wrapper import get_config
from h_rag.db.vector_db.pg_vector_wrapper import PgVectorWrapper
from h_rag.models.settings import get_settings


@pytest.fixture()
def wrapper(mocker: MockerFixture) -> PgVectorWrapper:
    """Provide a PgVectorWrapper with the embedding model bypassed."""
    mocker.patch(
        "h_rag.data_processing.embedding.Embedding.__init__", return_value=None, autospec=True
    )
    settings = get_settings()
    return PgVectorWrapper(
        db_name="test_postgres_db",
        user=settings.postgres_user,
        password=settings.postgres_password.get_secret_value(),
        host=get_config("postgres", "host"),
        port=int(get_config("postgres", "port")),
    )


@pytest.fixture
def db_cursor(wrapper: PgVectorWrapper):
    """Fixture to provide a database cursor."""
    with wrapper.connect_with_cursor() as (_, cur):
        yield cur


@pytest.fixture()
def kb_name() -> str:
    """Return the knowledge-base name used across create tests."""
    return "test_create_kb"


class TestPgVector:
    """Integration tests for PgVectorWrapper."""

    def test_create_inserts_knowledge_base(
        self, wrapper: PgVectorWrapper, kb_name: str, db_cursor
    ) -> None:
        """Test that create persists a new knowledge base row in the database."""
        # Act
        wrapper.create(kb_name)

        # Assert
        db_cursor.execute("SELECT name FROM knowledge_base WHERE name = %s;", (kb_name,))
        row = db_cursor.fetchone()

        assert row is not None
        assert row[0] == kb_name

    def test_create_is_idempotent(self, wrapper: PgVectorWrapper, kb_name: str, db_cursor) -> None:
        """Calling create twice with the same name results in one row, without raising an error."""
        # Act
        wrapper.create(kb_name)
        wrapper.create(kb_name)  # must not raise

        # Assert
        db_cursor.execute("SELECT COUNT(*) FROM knowledge_base WHERE name = %s;", (kb_name,))
        assert db_cursor.fetchone()[0] == 1

    def test_delete_removes_knowledge_base(
        self, wrapper: PgVectorWrapper, kb_name: str, db_cursor
    ) -> None:
        """Test that delete removes the knowledge base row from the database."""
        # Arrange
        wrapper.create(kb_name)
        db_cursor.execute("SELECT name FROM knowledge_base WHERE name = %s;", (kb_name,))
        assert db_cursor.fetchone() is not None  # Ensure it exists first

        # Act
        wrapper.delete(kb_name)

        # Assert
        db_cursor.execute("SELECT name FROM knowledge_base WHERE name = %s;", (kb_name,))
        row = db_cursor.fetchone()
        assert row is None

    def test_get_knowledge_bases_returns_names(self, wrapper: PgVectorWrapper, db_cursor) -> None:
        """Test that get_knowledge_bases returns the correct list of knowledge base names."""
        # Arrange
        names = ["kb1", "kb2", "kb3"]

        # Create knowledge bases
        for name in names:
            wrapper.create(name)

        # Act
        kb_list = wrapper.get_knowledge_bases()

        # Assert
        for name in names:
            assert name in kb_list
        assert len(kb_list) == len(names)
