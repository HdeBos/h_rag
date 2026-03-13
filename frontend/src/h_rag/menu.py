"""Sidebar menu for the Streamlit app."""

import streamlit as st


def menu():
    """Sidebar menu for the Streamlit app."""
    st.sidebar.page_link("chat.py", label="Chat")
    st.sidebar.page_link("pages/knowledge_base.py", label="Knowledge Base Management")
