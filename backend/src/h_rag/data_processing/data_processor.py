"""Module for data processing."""

import bisect

import fitz
from loguru import logger

from h_rag.chunking.chunking_factory import ChunkingFactory
from h_rag.models.document_data import DocumentData
from h_rag.models.file_data import FileData
from h_rag.object_storage.object_storage_factory import ObjectStorageFactory
from h_rag.vector_db.vector_db_factory import VectorDBFactory


class DataProcessor:
    """Class for processing data."""

    def process_file(self, file_data: FileData) -> DocumentData:
        """Process a single uploaded file."""
        self.store_file(file_data.data, file_data.name)
        text_per_page = self._get_text_per_page(file_data.data, file_data.type)
        text = "\n".join(text_per_page)
        page_offsets = self.get_offsets(text_per_page)
        chunker = ChunkingFactory.get_chunking_method()
        chunks = chunker.chunk(text)
        chunk_pages = self._get_chunk_pages(chunks, text, page_offsets)
        return DocumentData(
            data=file_data.data,
            name=file_data.name,
            type=file_data.type,
            chunks=chunks,
            chunk_pages=chunk_pages,
        )

    def store_data(self, file_data: DocumentData) -> None:
        """Store processed data in vector database."""
        vector_db = VectorDBFactory.get_vector_db()
        vector_db.create(file_data.name)
        vector_db.insert(
            name=file_data.name,
            chunks=file_data.chunks,
            doc_name=file_data.name,
            pages=file_data.chunk_pages,
        )
        logger.info(
            f"Stored {file_data.name} with {len(file_data.chunks)} chunks in vector database"
        )

    def store_file(self, file_data: bytes, file_name: str) -> None:
        """Store uploaded files in object storage."""
        object_storage = ObjectStorageFactory.get_object_storage()
        object_storage.upload_file(file_data=file_data, file_name=file_name)

    def _get_text_per_page(self, data: bytes, file_type: str) -> list[str]:
        """Extract the text for each page of the document."""
        with fitz.open(stream=data, filetype=file_type) as doc:
            text_per_page = [str(page.get_text("text")) for page in doc]
            logger.info(f"Successfully loaded document with {doc.page_count} pages")
            return text_per_page

    def get_offsets(self, text_per_page: list[str]) -> list[int]:
        """Get start offsets for each page."""
        offsets: list[int] = []
        pos = 0
        for page_text in text_per_page:
            offsets.append(pos)
            pos += len(page_text) + 1  # +1 for the "\n" separator
        return offsets

    def _get_chunk_pages(
        self, chunks: list[str], full_text: str, page_offsets: list[int]
    ) -> list[int]:
        """Map each chunk to its page number using a breadcrumb search."""
        pages = []
        pos = 0
        for chunk in chunks:
            idx = full_text.find(chunk[:40], pos)
            page = bisect.bisect_right(page_offsets, max(idx, 0)) - 1
            pages.append(page + 1)
            pos = max(idx, pos)
        return pages
