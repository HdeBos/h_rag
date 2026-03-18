"""Module for Pg vector database wrapper."""

import hashlib
from typing import override

from loguru import logger

from h_rag.db.postgres_wrapper import PostgresWrapper
from h_rag.db.vector_db.vector_db import VectorDB
from h_rag.models.vector_search_result import VectorSearchResult


class PgVectorWrapper(VectorDB, PostgresWrapper):
    """Wrapper for Pg vector database."""

    def __init__(self, db_name: str, user: str, password: str, host: str, port: int):
        """Initialize the pgvector database wrapper."""
        VectorDB.__init__(self)
        PostgresWrapper.__init__(
            self, db_name=db_name, user=user, password=password, host=host, port=port
        )

    @override
    def health_check(self) -> bool:
        try:
            with self.connect_with_cursor() as (_, cur):
                cur.execute("SELECT 1;")
                cur.fetchone()
            logger.info("PgVector health check successful")
            return True
        except Exception as e:
            logger.error(f"PgVector health check failed: {e}")
            return False

    @override
    def create(self, name: str) -> None:
        with self.connect_with_cursor() as (conn, cur):
            cur.execute(
                """
                INSERT INTO knowledge_base (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
                """,
                (name,),
            )
            conn.commit()

    @override
    def delete(self, name: str) -> None:
        with self.connect_with_cursor() as (conn, cur):
            cur.execute(
                """
                DELETE FROM knowledge_base
                WHERE name = %s;
                """,
                (name,),
            )
            conn.commit()

    @override
    def insert(
        self,
        name: str,
        chunks: list[str],
        doc_name: str,
        pages: list[int],
    ) -> None:
        # Encode outside the DB transaction to avoid holding the connection open during slow I/O
        embeddings = [self.embedding.encode(chunk, "document").tolist() for chunk in chunks]
        checksum = hashlib.sha256(doc_name.encode()).digest()

        with self.connect_with_cursor() as (conn, cur):
            cur.execute("SELECT id FROM knowledge_base WHERE name = %s;", (name,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Knowledge base '{name}' does not exist.")
            kb_id = row[0]

            # Insert document if not already present (deduplicate by checksum)
            cur.execute(
                """
                INSERT INTO document (title, checksum)
                VALUES (%s, %s)
                ON CONFLICT (checksum) DO NOTHING
                RETURNING id;
                """,
                (doc_name, checksum),
            )
            result = cur.fetchone()
            if result is None:
                cur.execute("SELECT id FROM document WHERE checksum = %s;", (checksum,))
                result = cur.fetchone()
            doc_id = result[0]  # pyright: ignore[reportOptionalSubscript]

            cur.execute(
                """
                INSERT INTO knowledge_base_document (knowledge_base_id, document_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (kb_id, doc_id),
            )

            cur.executemany(
                """
                INSERT INTO chunk (document_id, content, embedding, page_number)
                VALUES (%s, %s, %s::vector, %s);
                """,
                [
                    (doc_id, chunk, embedding, page)
                    for chunk, embedding, page in zip(chunks, embeddings, pages)
                ],
            )
            conn.commit()

    @override
    def query(self, name: str, query: str, n_results: int = 5) -> list[VectorSearchResult]:
        # Encode outside the DB transaction to avoid holding the connection open during slow I/O
        query_embedding = self.embedding.encode(query, "query").tolist()

        with self.connect_with_cursor() as (_, cur):
            cur.execute("SELECT id FROM knowledge_base WHERE name = %s;", (name,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Knowledge base '{name}' does not exist.")
            kb_id = row[0]

            cur.execute(
                """
                SELECT c.id, c.content, d.title, c.page_number
                FROM chunk c
                JOIN document d ON c.document_id = d.id
                JOIN knowledge_base_document kbd ON d.id = kbd.document_id
                WHERE kbd.knowledge_base_id = %s
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s;
                """,
                (kb_id, query_embedding, n_results),
            )
            rows = cur.fetchall()

        return [
            VectorSearchResult(id=str(row[0]), chunk=row[1], document=row[2], page=row[3])
            for row in rows
        ]

    @override
    def get_knowledge_bases(self) -> list[str]:
        with self.connect_with_cursor() as (_, cur):
            cur.execute("SELECT name FROM knowledge_base;")
            results = cur.fetchall()
            return [row[0] for row in results]
