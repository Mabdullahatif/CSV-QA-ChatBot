import streamlit as st
import pandas as pd
from agents_handler.agents import get_dynamic_agent
import os

def handle_file_upload(file_uploader_card):
    """
    Handles file upload, DataFrame creation, and session state updates.
    Returns True if a file was successfully uploaded and processed, else False.
    """
    llm_type = st.session_state.llm_type
    api_key = None
    if llm_type == "openai":
        api_key = st.session_state.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
    elif llm_type == "gemini":
        api_key = st.session_state.get("gemini_api_key") or os.getenv("GOOGLE_API_KEY")
    elif llm_type == "groq":
        api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")

    if not api_key:
        st.warning(f"Please enter your {llm_type.capitalize()} API key in the sidebar before uploading a CSV file.")
        st.file_uploader(
            "Choose a CSV file (API key required)",
            type="csv",
            help="Enter your API key in the sidebar first.",
            disabled=True
        )
        return False

    uploaded_file = file_uploader_card()
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.session_state.filename = uploaded_file.name
            st.session_state.agent = get_dynamic_agent(df, llm_type=llm_type, api_key=api_key)
            st.session_state.messages = [{
                "role": "assistant",
                "content": f"Hello! I've loaded your CSV file '{uploaded_file.name}' with {len(df)} rows and {len(df.columns)} columns. You can ask me questions about the data, request visualizations, or ask for data analysis. What would you like to know?"
            }]
            st.success(f"Successfully loaded {uploaded_file.name} with {len(df)} rows and {len(df.columns)} columns!")
            st.rerun()
            return True
        except ImportError as e:
            st.error(f"Import error: {str(e)}")
            st.session_state.df = pd.DataFrame()
            st.session_state.filename = None
            st.session_state.agent = None
            st.session_state.messages = []
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
            st.session_state.df = pd.DataFrame()
            st.session_state.filename = None
            st.session_state.agent = None
            st.session_state.messages = []
    return False 