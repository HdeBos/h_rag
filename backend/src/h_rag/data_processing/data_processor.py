"""Module for data processing."""

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
        text = self.extract_text(file_data.data, file_data.type)
        chunker = ChunkingFactory.get_chunking_method()
        chunks = chunker.chunk(text)
        document = DocumentData(
            data=file_data.data, name=file_data.name, type=file_data.type, chunks=chunks
        )
        return document

    def store_data(self, file_data: DocumentData) -> None:
        """Store processed data in vector database."""
        vector_db = VectorDBFactory.get_vector_db()
        vector_db.create(file_data.name)
        vector_db.insert(name=file_data.name, chunks=file_data.chunks)
        logger.info(
            f"Stored {file_data.name} with {len(file_data.chunks)} chunks in vector database"
        )

    def store_file(self, file_data: bytes, file_name: str) -> None:
        """Store uploaded files in object storage."""
        object_storage = ObjectStorageFactory.get_object_storage()
        object_storage.upload_file(file_data=file_data, file_name=file_name)

    def extract_text(self, data: bytes, file_type: str) -> str:
        """Extract text from a file."""
        with fitz.open(stream=data, filetype=file_type) as doc:
            text = [str(page.get_text("text")) for page in doc]
        return "\n".join(text)
