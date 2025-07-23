import streamlit as st
import pandas as pd
from agents_handler.agents import get_dynamic_agent

def handle_file_upload(file_uploader_card):
    """
    Handles file upload, DataFrame creation, and session state updates.
    Returns True if a file was successfully uploaded and processed, else False.
    """
    uploaded_file = file_uploader_card()
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.session_state.filename = uploaded_file.name
            st.session_state.agent = get_dynamic_agent(df, llm_type=st.session_state.llm_type)
            st.session_state.messages = [{
                "role": "assistant",
                "content": f"Hello! I've loaded your CSV file '{uploaded_file.name}' with {len(df)} rows and {len(df.columns)} columns. You can ask me questions about the data, request visualizations, or ask for data analysis. What would you like to know?"
            }]
            st.success(f"Successfully loaded {uploaded_file.name} with {len(df)} rows and {len(df.columns)} columns!")
            st.rerun()
            return True
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
    return False 