"""Shared fixtures for db integration tests."""

from collections.abc import Generator

import pytest
from psycopg import sql

from h_rag.db.vector_db.pg_vector_wrapper import PgVectorWrapper


@pytest.fixture(autouse=True)
def cleanup_db(wrapper: PgVectorWrapper) -> Generator[None, None, None]:
    """Truncate all public tables after each test to guarantee isolation."""
    yield
    with wrapper.connect_with_cursor() as (conn, cur):
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
