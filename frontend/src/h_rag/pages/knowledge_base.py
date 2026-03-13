"""Knowledge base management page for the Streamlit app."""

import base64

import requests
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from h_rag.menu import menu


def get_knowledge_bases() -> list[str]:
    """Get the knowledge bases from the vector database."""
    knowledge_bases = requests.get("http://backend:8000/knowledge-bases")
    return knowledge_bases.json()


def delete_knowledge_base(knowledge_base_name: str) -> None:
    """Delete the selected knowledge base."""
    requests.delete(f"http://backend:8000/knowledge-bases/{knowledge_base_name}")
    st.success(f"Deleted knowledge base: {knowledge_base_name}")


def process_files(uploaded_files: list[UploadedFile]) -> None:
    """Process the uploaded files and add them to the knowledge base."""
    if not uploaded_files:
        st.warning("Please upload at least one file.")
        return

    for file in uploaded_files:
        file_bytes = file.read()
        file_b64 = base64.b64encode(file_bytes).decode("utf-8")
        file_data = {
            "name": file.name,
            "data": file_b64,
            "type": file.type,
        }
        resp = requests.post("http://backend:8000/knowledge-bases/", json=file_data)
        if not resp.ok:
            st.error(f"Failed to upload {file.name}: {resp.text}")

    st.success("Processed files")


if __name__ == "__main__":
    st.set_page_config(page_title="Knowledge Base Management", layout="wide")
    menu()
    uploaded_files = st.file_uploader(
        "Upload a file to add to the knowledge base",
        type=["pdf"],
        accept_multiple_files=True,
    )

    st.button("Process Uploaded Files", on_click=process_files, args=(uploaded_files,))

    knowledge_base = st.selectbox("Knowledge base to delete", options=get_knowledge_bases())
    st.button("Delete Knowledge Base", on_click=delete_knowledge_base, args=(knowledge_base,))
