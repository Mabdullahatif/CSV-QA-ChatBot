import streamlit as st
import pandas as pd
from io import StringIO
from agents_handler.agents import get_dynamic_agent
import plotly.graph_objects as go
import plotly.express as px
import re
import sys
import io
from custom_css.apply_custom_css import apply_custom_css
import os
import time
from dotenv import load_dotenv
from ui_components.sidebar import sidebar
from ui_components.file_loader import file_uploader_card
from ui_components.extras import show_feature_cards
from ui_components.header import show_header
from ui_components.file_upload import handle_file_upload
from ui_components.data_preview import render_data_preview_tab
from ui_components.chat_analysis import render_chat_analysis_tab

load_dotenv()
# --- Get API keys from environment variables ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# --- Apply custom CSS ---
st.markdown(apply_custom_css(), unsafe_allow_html=True)

# --- Session State ---
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'filename' not in st.session_state:
    st.session_state.filename = None
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'llm_type' not in st.session_state:
    st.session_state.llm_type = "gemini"


# --- Sidebar ---
sidebar()

# --- Main Header ---
show_header()

# --- Main Content ---
if st.session_state.df.empty:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload CSV File")
    if handle_file_upload(file_uploader_card):
        pass  # rerun is handled inside handle_file_upload
    show_feature_cards()
else:
    tabs = st.tabs(["Data Preview", "Chat Analysis"])
    with tabs[0]:
        render_data_preview_tab(st.session_state.df, st.session_state.filename)
    with tabs[1]:
        render_chat_analysis_tab(st.session_state.messages, st.session_state.agent, st.session_state.df)