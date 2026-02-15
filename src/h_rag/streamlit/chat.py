"""Chat page for the Streamlit app."""

import streamlit as st

from h_rag.llm.llm import LLM
from h_rag.llm.llm_factory import LLMFactory
from h_rag.streamlit.menu import menu
from h_rag.tools import initialize_logger, load_env
from h_rag.vector_db.vector_db_factory import VectorDBFactory
from h_rag.workflows.workflow_factory import WorkflowFactory


def get_knowledge_base() -> str:
    """Get the knowledge base from the vector database."""
    if "knowledge_bases" not in st.session_state:
        vector_db = VectorDBFactory.get_vector_db()
        st.session_state.knowledge_bases = vector_db.get_knowledge_bases()
    knowledge_base = st.sidebar.selectbox(
        "Select a knowledge base", options=st.session_state.knowledge_bases
    )
    return knowledge_base


def get_model(llm: LLM) -> str:
    """Get the model from the sidebar selection."""
    if not "models" in st.session_state:
        st.session_state.models = llm.get_models()
    model = st.sidebar.selectbox("Select a model", options=st.session_state.models)
    return model


def get_llm() -> LLM:
    """Get the LLM instance from the session state or create a new one."""
    if "llm" not in st.session_state:
        st.session_state.llm = LLMFactory.get_llm()
    llm = st.session_state.llm
    return llm


if __name__ == "__main__":
    load_env()
    initialize_logger()
    st.set_page_config(page_title="Chat", layout="wide")
    menu()
    st.sidebar.markdown("<div style='height:50vh'></div>", unsafe_allow_html=True)
    llm = get_llm()
    model = get_model(llm)
    knowledge_base = get_knowledge_base()
    workflow = WorkflowFactory.get_workflow(model, knowledge_base)
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
            response = workflow.execute(prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

    else:
        for msg in st.session_state.messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            with st.chat_message(role):
                st.write(content)
