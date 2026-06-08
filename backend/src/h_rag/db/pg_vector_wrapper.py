"""Module for Pg vector database wrapper."""

import hashlib

from h_rag.data_processing.embedding import Embedding
from h_rag.db.postgres_wrapper import PostgresWrapper
from h_rag.models.vector_search_result import VectorSearchResult


class PgVectorWrapper:
    """Wrapper for Pg vector database."""

    def __init__(self, pg: PostgresWrapper):
        """Initialize the pgvector database wrapper."""
        self.pg = pg
        self.embedding = Embedding()

    def _get_document_id(self, doc_name: str) -> int:
        """Get the document ID for a given document name.

        Args:
            doc_name: The name of the document.

        Returns:
            The ID of the document.
        """
        with self.pg.get_connection() as (_, cur):
            cur.execute(
                """
                SELECT id FROM document
                WHERE name = %s;
                """,
                (doc_name,),
            )
            result = cur.fetchone()
            if result is None:
                raise ValueError(f"Document with name '{doc_name}' not found.")
            return result[0]

    def _get_kb_id(self, kb_name: str) -> int:
        """Get the knowledge base ID for a given knowledge base name.

        Args:
            kb_name: The name of the knowledge base.

        Returns:
            The ID of the knowledge base.
        """
        with self.pg.get_connection() as (_, cur):
            cur.execute(
                """
                SELECT id FROM knowledge_base
                WHERE name = %s;
                """,
                (kb_name,),
            )
            result = cur.fetchone()
            if result is None:
                raise ValueError(f"Knowledge base with name '{kb_name}' not found.")
            return result[0]

    def create(self, name: str) -> None:
        """Create a knowledge base.

        Args:
            name: The name of the knowledge base to create.
        """
        with self.pg.get_connection() as (conn, cur):
            cur.execute(
                """
                INSERT INTO knowledge_base (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
                """,
                (name,),
            )
            conn.commit()

    def delete(self, name: str) -> None:
        """Delete a knowledge base.

        Args:
            name: The name of the knowledge base to delete.
        """
        with self.pg.get_connection() as (conn, cur):
            cur.execute(
                """
                DELETE FROM knowledge_base
                WHERE name = %s;
                """,
                (name,),
            )
            conn.commit()

    def insert(
        self,
        name: str,
        chunks: list[str],
        doc_name: str,
        pages: list[int],
    ) -> None:
        """Add chunks to a knowledge base.

        Args:
            name: The name of the knowledge base to add chunks to.
            chunks: The list of chunks to add.
            doc_name: The name of the document the chunks belong to.
            pages: The list of page numbers corresponding to each chunk.
        """
        # Encode outside the DB transaction to avoid holding the connection open during slow I/O
        embeddings = [self.embedding.encode(chunk, "document").tolist() for chunk in chunks]
        checksum = hashlib.sha256(doc_name.encode()).digest()

        with self.pg.get_connection() as (conn, cur):
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

    def query(self, name: str, query: str, n_results: int = 5) -> list[VectorSearchResult]:
        """Query a knowledge base.

        Args:
            name: The name of the knowledge base to query.
            query: The query string to search for.
            n_results: The number of results to return.

        Returns:
            A list of results from the knowledge base.
        """
        # Encode outside the DB transaction to avoid holding the connection open during slow I/O
        query_embedding = self.embedding.encode(query, "query").tolist()

        with self.pg.get_connection() as (_, cur):
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

    def get_knowledge_bases(self) -> list[str]:
        """Get all knowledge bases.

        Returns:
            A list of all knowledge bases.
        """
        with self.pg.get_connection() as (_, cur):
            cur.execute("SELECT name FROM knowledge_base;")
            results = cur.fetchall()
            return [row[0] for row in results]

    def get_documents(self) -> list[str]:
        """Get all documents.

        Returns:
            A list of all documents.
        """
        with self.pg.get_connection() as (_, cur):
            cur.execute("SELECT title FROM document;")
            results = cur.fetchall()
            return [row[0] for row in results]

    def add_document_to_kb(self, kb_name: str, doc_name: str) -> None:
        """Add a document to a knowledge base in the knowledge_base_document table.

        Args:
            kb_name: The name of the knowledge base.
            doc_name: The name of the document.
        """
        kb_id = self._get_kb_id(kb_name)
        doc_id = self._get_document_id(doc_name)
        with self.pg.get_connection() as (conn, cur):
            cur.execute(
                """
                INSERT INTO knowledge_base_document (knowledge_base_id, document_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (kb_id, doc_id),
            )
            conn.commit()

    def remove_document_from_kb(self, kb_name: str, doc_name: str) -> None:
        """Remove a document from a knowledge base in the knowledge_base_document table.

        Args:
            kb_name: The name of the knowledge base.
            doc_name: The name of the document.
        """
        kb_id = self._get_kb_id(kb_name)
        doc_id = self._get_document_id(doc_name)
        with self.pg.get_connection() as (conn, cur):
            cur.execute(
                """
                DELETE FROM knowledge_base_document
                WHERE knowledge_base_id = %s AND document_id = %s;
                """,
                (kb_id, doc_id),
            )
            conn.commit()
