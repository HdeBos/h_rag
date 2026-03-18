"""Shared fixtures for integration tests."""

from pathlib import Path
from typing import Any

import pytest
from psycopg import sql

from h_rag.config.config_wrapper import get_config
from h_rag.db.postgres_wrapper import PostgresWrapper
from h_rag.models.settings import get_settings

_INIT_SQL = Path(__file__).parents[3] / "db" / "init.sql"


def terminate_db_connections(cur: Any, db_name: str) -> None:
    """Terminate all connections to the given database except the current one."""
    cur.execute(
        """
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = %s
        AND pid <> pg_backend_pid();
        """,
        (db_name,),
    )


@pytest.fixture(scope="session")
def postgres_wrapper():
    """Factory fixture to create a PostgresWrapper for any db_name."""
    settings = get_settings()

    def _factory(db_name: str) -> PostgresWrapper:
        return PostgresWrapper(
            db_name=db_name,
            user=settings.postgres_user,
            password=settings.postgres_password.get_secret_value(),
            host=get_config("postgres", "host"),
            port=int(get_config("postgres", "port")),
        )

    return _factory


@pytest.fixture(autouse=True, scope="session")
def create_test_db(check_postgres_connection, postgres_wrapper):
    """Fixture to initialize and cleanup the test database."""
    db_name = "test_postgres_db"
    admin_wrapper = postgres_wrapper(get_settings().postgres_db)
    with admin_wrapper.connect_raw() as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            terminate_db_connections(cur, db_name)
            cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name)))
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    # Initialize the schema in the new database
    test_wrapper = postgres_wrapper(db_name)
    with test_wrapper.connect_with_cursor() as (conn, cur):
        cur.execute(_INIT_SQL.read_text())
        conn.commit()
    yield

    admin_wrapper = postgres_wrapper(get_settings().postgres_db)
    with admin_wrapper.connect_raw() as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            terminate_db_connections(cur, db_name)
            cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name)))


@pytest.fixture(scope="session")
def check_postgres_connection(postgres_wrapper):
    """Check that a connection can be made to Postgres."""
    admin_wrapper = postgres_wrapper(get_settings().postgres_db)
    try:
        with admin_wrapper.connect_with_cursor() as (_, cur):
            cur.execute("SELECT 1;")
            assert cur.fetchone() == (1,)
    except Exception as e:
        raise RuntimeError(f"Could not connect to admin Postgres DB: {e}")
