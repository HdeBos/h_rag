"""Knowledge base management page for the Streamlit app."""

import streamlit as st

from h_rag.data_processing.data_processor import DataProcessor
from h_rag.streamlit.menu import menu


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
