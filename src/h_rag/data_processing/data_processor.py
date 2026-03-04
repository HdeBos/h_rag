"""Module for data processing."""

import fitz
from loguru import logger
from streamlit.runtime.uploaded_file_manager import UploadedFile

from h_rag.chunking.chunking_factory import ChunkingFactory
from h_rag.models.document_data import DocumentData
from h_rag.object_storage.object_storage_factory import ObjectStorageFactory
from h_rag.vector_db.vector_db_factory import VectorDBFactory


class DataProcessor:
    """Class for processing data."""

    def process_files(self, files: list[UploadedFile]) -> None:
        """Process uploaded files."""
        for file in files:
            file_data = self.process_file(file)
            self.store_data(file_data)

    def process_file(self, file: UploadedFile) -> DocumentData:
        """Process a single uploaded file."""
        self.store_file(file)
        text = self.extract_text(file.getvalue(), file.type)
        chunker = ChunkingFactory.get_chunking_method()
        chunks = chunker.chunk(text)
        file_data = DocumentData(
            data=file.getvalue(), name=file.name, type=file.type, chunks=chunks
        )
        return file_data

    def store_data(self, file_data: DocumentData) -> None:
        """Store processed data in vector database."""
        vector_db = VectorDBFactory.get_vector_db()
        vector_db.create(file_data.name)
        vector_db.insert(name=file_data.name, chunks=file_data.chunks)
        logger.info(
            f"Stored {file_data.name} with {len(file_data.chunks)} chunks in vector database"
        )

    def store_file(self, file: UploadedFile) -> None:
        """Store uploaded files in object storage."""
        object_storage = ObjectStorageFactory.get_object_storage()
        object_storage.upload_file(file_data=file.getvalue(), file_name=file.name)

    def extract_text(self, data: bytes, file_type: str) -> str:
        """Extract text from a file."""
        with fitz.open(stream=data, filetype=file_type) as doc:
            text = [str(page.get_text("text")) for page in doc]
        return "\n".join(text)
