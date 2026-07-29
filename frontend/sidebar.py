import uuid
import streamlit as st

from database.models import (
    create_chat,
    get_all_chats,
)


def initialize_session():
    """Initialize session state."""

    if "current_thread" not in st.session_state:
        st.session_state.current_thread = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Track which chat is currently loaded
    if "loaded_thread" not in st.session_state:
        st.session_state.loaded_thread = None


def create_new_chat():
    """Create a new chat."""

    thread_id = str(uuid.uuid4())

    create_chat(
        title="New Chat",
        thread_id=thread_id,
    )

    st.session_state.current_thread = thread_id
    st.session_state.loaded_thread = None
    st.session_state.messages = []

    st.rerun()


def select_chat(thread_id: str):
    """Switch to another chat."""

    st.session_state.current_thread = thread_id

    # Force chat reload
    st.session_state.loaded_thread = None

    st.rerun()


def render_sidebar():

    initialize_session()

    st.sidebar.title("🤖 AI Assistant")

    st.sidebar.divider()

    if st.sidebar.button(
        "➕ New Chat",
        use_container_width=True,
    ):
        create_new_chat()

    st.sidebar.divider()

    st.sidebar.subheader("Chats")

    chats = get_all_chats()

    if len(chats) == 0:

        st.sidebar.info(
            "Create your first chat."
        )

    else:

        for chat in chats:

            is_current = (
                chat["thread_id"] ==
                st.session_state.current_thread
            )

            label = (
                f"💬 {chat['title']}"
                if is_current
                else chat["title"]
            )

            if st.sidebar.button(
                label,
                key=chat["thread_id"],
                use_container_width=True,
            ):
                select_chat(chat["thread_id"])

    st.sidebar.divider()

    st.sidebar.subheader("Settings")

    st.sidebar.selectbox(
        "Model",
        [
            "Llama 3.3 70B"
        ],
    )

    st.sidebar.slider(
        "Temperature",
        0.0,
        1.0,
        0.7,
    )