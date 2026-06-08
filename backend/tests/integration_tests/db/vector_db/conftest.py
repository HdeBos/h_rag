"""Shared fixtures for db integration tests."""

from collections.abc import Generator

import pytest
from psycopg import sql

from h_rag.db.postgres_wrapper import PostgresWrapper


@pytest.fixture(autouse=True)
def cleanup_db(postgres_connection: PostgresWrapper) -> Generator[None, None, None]:
    """Truncate all public tables after each test to guarantee isolation."""
    yield
    with postgres_connection.get_connection() as (conn, cur):
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """
        )
        table_names = [row[0] for row in cur.fetchall()]
        if table_names:
            stmt = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE;").format(
                sql.SQL(", ").join(sql.Identifier(t) for t in table_names)
            )
            cur.execute(stmt)
            conn.commit()
