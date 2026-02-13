"""Sidebar menu for the Streamlit app."""

import streamlit as st


def menu():
    """Sidebar menu for the Streamlit app."""
    st.sidebar.page_link("main.py", label="Home")
    st.sidebar.page_link("pages/chat.py", label="Chat")
