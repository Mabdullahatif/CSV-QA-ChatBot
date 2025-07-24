import os
from langchain_community.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq 
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

def get_dynamic_agent(df, llm_type="openai", temperature=0, api_key=None):
    """
    Returns a LangChain agent for a given DataFrame using the selected LLM.
    llm_type: "openai", "gemini", or "groq"
    api_key: Optional. If not provided, will check Streamlit session_state, then environment variable.
    """
    if llm_type == "openai":
        key = api_key or st.session_state.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OpenAI API key not set. Please enter your key in the sidebar.")
        llm = OpenAI(model="gpt-4o-mini", temperature=temperature, api_key=key)
    elif llm_type == "gemini":
        key = api_key or st.session_state.get("gemini_api_key") or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ValueError("Google Gemini API key not set. Please enter your key in the sidebar.")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature, api_key=key)
    elif llm_type == "groq":
        key = api_key or st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("Groq API key not set. Please enter your key in the sidebar.")
        llm = ChatGroq(model="llama3-70b-8192", temperature=temperature, groq_api_key=key)
    else:
        raise ValueError("Unsupported LLM type. Choose 'openai', 'gemini', or 'groq'.")

    agent = create_pandas_dataframe_agent(
        llm, df, verbose=True, allow_dangerous_code=True, handle_parsing_errors=True
    )
    return agent