"""Chat page for the Streamlit app."""

import requests
import streamlit as st

from h_rag.menu import menu


def get_knowledge_base() -> str:
    """Get the knowledge bases from the vector database."""
    knowledge_bases = requests.get("http://backend:8000/knowledge-bases")
    knowledge_base = st.sidebar.selectbox("Select a knowledge base", options=knowledge_bases.json())
    return knowledge_base


def get_model() -> str:
    """Get the model from the sidebar selection."""
    models = requests.get("http://backend:8000/chat/models")
    selected = st.sidebar.selectbox("Select model", options=models.json())
    return selected if selected is not None else ""


def get_highlighted_file(file_name: str, highlight: str) -> str:
    """Get a file from the knowledge base, with the relevant chunk highlighted."""
    file_data = requests.get(f"http://backend:8000/knowledge-bases/files/{file_name}/{highlight}")
    file_data = file_data.json()
    return file_data


if __name__ == "__main__":
    st.set_page_config(page_title="Chat", layout="wide")
    menu()
    st.sidebar.markdown("<div style='height:50vh'></div>", unsafe_allow_html=True)
    model = get_model()
    knowledge_base = get_knowledge_base()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    query = st.chat_input("Ask anything...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})

        for msg in st.session_state.messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            with st.chat_message(role):
                st.markdown(content, unsafe_allow_html=True)

        with st.spinner("Crafting response..."):
            response_data = requests.post(
                "http://backend:8000/chat/query",
                json={
                    "query": query,
                    "model": model,
                    "knowledge_base": knowledge_base,
                },
            ).json()
            file_name = response_data.get("document", {})
            response = response_data.get("response", "No response from server.")
            chunk = response_data.get("chunk", "")
            page = response_data.get("page", 0)
            if file_name:
                file_data = get_highlighted_file(file_name, chunk)
                pdf_url = f"data:application/pdf;base64,{file_data}#page={page}"
                response = (
                    f"{response}\n\n<small><a href='{pdf_url}' target='_blank'>Source</a></small>"
                )

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)

    else:
        for msg in st.session_state.messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            with st.chat_message(role):
                st.markdown(content, unsafe_allow_html=True)
