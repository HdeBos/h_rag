"""Chat page for the Streamlit app."""

import streamlit as st

from h_rag.config.config_wrapper import get_config
from h_rag.llm.llm import LLM
from h_rag.llm.llm_factory import LLMFactory
from h_rag.streamlit.menu import menu


def get_model(llm: LLM) -> str:
    """Get the model from the sidebar selection."""
    if not "models" in st.session_state:
        st.session_state.models = llm.get_models()
    st.sidebar.markdown("<div style='height:60vh'></div>", unsafe_allow_html=True)
    model = st.sidebar.selectbox("Select a model", options=st.session_state.model)
    return model


def get_llm() -> LLM:
    """Get the LLM instance from the session state or create a new one."""
    if "llm" not in st.session_state:
        st.session_state.llm = LLMFactory.get_llm(get_config("llm_provider"))
    llm = st.session_state.llm
    return llm


if __name__ == "__main__":
    st.set_page_config(page_title="Chat", layout="wide")
    menu()
    llm = get_llm()
    model = get_model(llm)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    prompt = st.chat_input("Ask anything...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        for msg in st.session_state.messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            with st.chat_message(role):
                st.write(content)

        with st.spinner("Crafting response..."):
            response = llm.query(model, prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

    else:
        for msg in st.session_state.messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            with st.chat_message(role):
                st.write(content)
