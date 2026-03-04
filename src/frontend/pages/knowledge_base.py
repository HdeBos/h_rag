"""Knowledge base management page for the Streamlit app."""

import streamlit as st

from frontend.menu import menu
from h_rag.data_processing.data_processor import DataProcessor
from h_rag.object_storage.object_storage_factory import ObjectStorageFactory
from h_rag.vector_db.vector_db_factory import VectorDBFactory


def get_knowledge_bases() -> None:
    """Get the knowledge base from the vector database."""
    if "knowledge_bases" not in st.session_state:
        vector_db = VectorDBFactory.get_vector_db()
        st.session_state.knowledge_bases = vector_db.get_knowledge_bases()


def delete_knowledge_base(knowledge_base: str):
    """Delete the selected knowledge base."""
    vector_db = VectorDBFactory.get_vector_db()
    vector_db.delete(knowledge_base)
    object_storage = ObjectStorageFactory.get_object_storage()
    object_storage.delete_file(knowledge_base)
    st.success(f"Deleted knowledge base: {knowledge_base}")


def init():
    """Initialize the knowledge base management page."""
    if not "data_processor" in st.session_state:
        st.session_state.data_processor = DataProcessor()


def process_files(uploaded_files):
    """Process the uploaded files and add them to the knowledge base."""
    if not uploaded_files:
        st.warning("Please upload at least one file.")
        return

    st.session_state.data_processor.process_files(uploaded_files)
    st.success(f"Processed files")


if __name__ == "__main__":
    st.set_page_config(page_title="Knowledge Base Management", layout="wide")
    menu()
    init()
    uploaded_files = st.file_uploader(
        "Upload a file to add to the knowledge base",
        type=["pdf"],
        accept_multiple_files=True,
    )

    st.button("Process Uploaded Files", on_click=process_files, args=(uploaded_files,))
    get_knowledge_bases()
    knowledge_base = st.selectbox(
        "Knowledge base to delete", options=st.session_state.knowledge_bases
    )
    st.button("Delete Knowledge Base", on_click=delete_knowledge_base, args=(knowledge_base,))
