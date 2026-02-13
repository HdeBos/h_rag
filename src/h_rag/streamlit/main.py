"""Main entry point for the Streamlit app."""

import streamlit as st

from h_rag.streamlit.menu import menu
from h_rag.tools import initialize_logger, load_env

if __name__ == "__main__":
    load_env()
    initialize_logger()
    st.set_page_config(page_title="main", layout="wide")
    menu()
    st.title("H_RAG")
