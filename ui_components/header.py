import streamlit as st

def show_header():
    st.markdown('<div class="main-header">🤖 CSV Q/A ChatBot</div>', unsafe_allow_html=True)
    st.markdown("Upload a CSV file and chat with your data using AI")
    st.markdown("---")