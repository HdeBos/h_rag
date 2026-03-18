"""Wrapper for Postgres database, to store functionality required for all postgres operations."""

from contextlib import contextmanager
from typing import Any

import psycopg


class PostgresWrapper:
    """Wrapper for Postgres database."""

    def __init__(self, db_name: str, user: str, password: str, host: str, port: int):
        """Initialize the Postgres database wrapper."""
        self.conn_params: dict[str, Any] = {
            "dbname": db_name,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
            "connect_timeout": 5,
        }

    @contextmanager
    def connect_with_cursor(self):
        """Provide a context manager for both connection and cursor."""
        conn = psycopg.connect(**self.conn_params)
        try:
            with conn.cursor() as cur:
                yield conn, cur
        finally:
            conn.close()

    @contextmanager
    def connect_raw(self):
        """Provide a context manager for raw connection."""
        conn = psycopg.connect(**self.conn_params)
        try:
            yield conn
        finally:
            conn.close()
