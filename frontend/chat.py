import streamlit as st
from langchain_core.messages import HumanMessage

from backend.graph import chatbot
from database.models import (
    get_chat_by_thread,
    get_messages,
    save_message,
    update_chat_title,
)


def initialize_chat():
    """Initialize chat session state."""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_thread" not in st.session_state:
        st.session_state.current_thread = None

    if "loaded_thread" not in st.session_state:
        st.session_state.loaded_thread = None


def load_chat_messages():
    """
    Load messages only when a different chat is selected.
    """

    if st.session_state.current_thread is None:
        return

    # Already loaded
    if (
        st.session_state.loaded_thread
        == st.session_state.current_thread
    ):
        return

    chat = get_chat_by_thread(
        st.session_state.current_thread
    )

    if chat is None:
        return

    db_messages = get_messages(chat["id"])

    st.session_state.messages = []

    for msg in db_messages:

        st.session_state.messages.append(
            {
                "role": msg["role"],
                "content": msg["content"],
            }
        )

    st.session_state.loaded_thread = (
        st.session_state.current_thread
    )


def display_messages():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():

    prompt = st.chat_input(
        "Type your message..."
    )

    if not prompt:
        return

    if st.session_state.current_thread is None:
        st.warning("Please create a new chat first.")
        return

    # ------------------------
    # User Message
    # ------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    chat = get_chat_by_thread(
        st.session_state.current_thread
    )
    
    if chat["title"] == "New Chat":

        title = prompt.strip()

        if len(title) > 40:
            title = title[:40] + "..."

        update_chat_title(
            st.session_state.current_thread,
            title,
        )

        chat = get_chat_by_thread(
            st.session_state.current_thread
        )

    save_message(
        chat["id"],
        "user",
        prompt,
    )

    # ------------------------
    # Assistant Response
    # ------------------------

    with st.chat_message("assistant"):

        response = st.write_stream(

            chunk.content

            for chunk, metadata in chatbot.stream(

                {
                    "messages": [
                        HumanMessage(content=prompt)
                    ]
                },

                config={
                    "configurable": {
                        "thread_id": st.session_state.current_thread
                    }
                },

                stream_mode="messages",
            )
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    save_message(
        chat["id"],
        "assistant",
        response,
    )


def render_chat():

    initialize_chat()

    load_chat_messages()

    display_messages()

    handle_user_input()