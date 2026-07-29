import streamlit as st

from database.models import initialize_database

from frontend.styles import load_css
from frontend.sidebar import render_sidebar
from frontend.chat import render_chat


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
)

# =====================================================
# INITIALIZE DATABASE
# =====================================================

initialize_database()

# =====================================================
# LOAD CSS
# =====================================================

load_css()

# =====================================================
# SIDEBAR
# =====================================================

render_sidebar()

# =====================================================
# HEADER
# =====================================================

st.title("🤖 AI Assistant")

st.caption("Powered by LangGraph + Groq")

st.divider()

# =====================================================
# CHAT
# =====================================================

render_chat()