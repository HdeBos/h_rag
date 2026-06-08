"""Wrapper for Postgres database, to store functionality required for all postgres operations."""

from contextlib import contextmanager
from typing import Any

from loguru import logger
from psycopg_pool import ConnectionPool


class PostgresWrapper:
    """Wrapper for Postgres database."""

    def __init__(
        self,
        db_name: str,
        user: str,
        password: str,
        host: str,
        port: int,
        min_size: int = 0,
        max_size: int = 10,
    ):
        """Initialize the Postgres database wrapper."""
        self.conn_params: dict[str, Any] = {
            "dbname": db_name,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
            "connect_timeout": 5,
        }
        self._pool: ConnectionPool = ConnectionPool(
            kwargs=self.conn_params, min_size=min_size, max_size=max_size, open=True
        )

    def health_check(self) -> bool:
        """Check if the Postgres database is healthy and can be reached."""
        try:
            with self.get_connection() as (_, cur):
                cur.execute("SELECT 1;")
                cur.fetchone()
            logger.info("Postgres health check successful")
            return True
        except Exception as e:
            logger.error(f"Postgres health check failed: {e}")
            return False

    @contextmanager
    def get_connection(self):
        """Provide a context manager for both connection and cursor."""
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                yield conn, cur

    @contextmanager
    def connect_raw(self):
        """Provide a context manager for both connection and cursor."""
        with self._pool.connection() as conn:
            yield conn

    def close(self) -> None:
        """Close the connection pool and release all held connections."""
        self._pool.close()
