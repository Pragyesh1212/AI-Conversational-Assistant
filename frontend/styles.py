import streamlit as st


def load_css():
    st.markdown("""
    <style>

    /* Main content */
    .block-container{
        padding-top:1.5rem;
        padding-bottom:2rem;
        max-width:1000px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"]{
        width:300px !important;
    }

    /* Chat input */
    div[data-testid="stChatInput"]{
        max-width:1000px;
        margin:0 auto;
    }

    /* Code blocks */
    pre{
        border-radius:12px;
    }

    code{
        font-size:15px;
    }

    </style>
    """, unsafe_allow_html=True)