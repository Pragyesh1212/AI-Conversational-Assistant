import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from backend.graph import chatbot
from database.models import (
    get_chat_by_thread,
    get_messages,
    save_message,
    update_chat_title,
)


def initialize_chat():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_thread" not in st.session_state:
        st.session_state.current_thread = None

    if "loaded_thread" not in st.session_state:
        st.session_state.loaded_thread = None

    if "pending_interrupt" not in st.session_state:
        st.session_state.pending_interrupt = None


def load_chat_messages():

    if st.session_state.current_thread is None:
        return

    if st.session_state.loaded_thread == st.session_state.current_thread:
        return

    chat = get_chat_by_thread(
        st.session_state.current_thread
    )

    if chat is None:
        return

    db_messages = get_messages(chat["id"])

    st.session_state.messages = []

    for msg in db_messages:
        st.session_state.messages.append({
            "role": msg["role"],
            "content": msg["content"],
        })

    st.session_state.loaded_thread = st.session_state.current_thread


def display_messages():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_pending_approval():

    if st.session_state.pending_interrupt is None:
        return

    question = st.session_state.pending_interrupt

    st.warning(
        f"⚠️ Human approval required: {question}"
    )

    col1, col2 = st.columns(2)

    with col1:
        approve = st.button(
            "✅ Approve",
            use_container_width=True,
        )

    with col2:
        reject = st.button(
            "❌ Reject",
            use_container_width=True,
        )

    if approve or reject:

        decision = "yes" if approve else "no"

        result = chatbot.invoke(
            Command(resume=decision),
            config={
                "configurable": {
                    "thread_id": st.session_state.current_thread
                }
            },
        )

        st.session_state.pending_interrupt = None

        response = result["messages"][-1].content

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
        })

        chat = get_chat_by_thread(
            st.session_state.current_thread
        )

        save_message(
            chat["id"],
            "assistant",
            response,
        )

        st.rerun()


def handle_user_input():

    if st.session_state.pending_interrupt is not None:
        return

    prompt = st.chat_input(
        "Type your message..."
    )

    if not prompt:
        return

    if st.session_state.current_thread is None:
        st.warning("Please create a new chat first.")
        return

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

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

    with st.chat_message("assistant"):

        result = chatbot.invoke(
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
        )

        interrupts = result.get("__interrupt__", [])

        if interrupts:

            st.session_state.pending_interrupt = (
                interrupts[0].value
            )

            st.rerun()

        response = result["messages"][-1].content

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })

    save_message(
        chat["id"],
        "assistant",
        response,
    )


def render_chat():

    initialize_chat()
    load_chat_messages()
    display_messages()
    handle_pending_approval()
    handle_user_input()
