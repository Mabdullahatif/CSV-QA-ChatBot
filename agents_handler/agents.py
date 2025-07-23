import os
from langchain_community.llms import OpenAI
#from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq  # NEW: Import ChatGroq
from dotenv import load_dotenv
load_dotenv()

def get_dynamic_agent(df, llm_type="openai", temperature=0):
    """
    Returns a LangChain agent for a given DataFrame using the selected LLM.
    llm_type: "openai" or "gemini"
    """
    if llm_type == "openai":
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        llm = OpenAI(model="gpt-4o-mini", temperature=temperature, api_key=openai_api_key)
    elif llm_type == "gemini":
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY envir  onment variable not set.")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature, api_key=google_api_key)
    elif llm_type == "groq":  # NEW: Add Groq support
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        llm = ChatGroq(model="llama3-70b-8192", temperature=temperature, groq_api_key=groq_api_key)
    else:
        raise ValueError("Unsupported LLM type. Choose 'openai', 'gemini', or 'groq'.")

    agent = create_pandas_dataframe_agent(
        llm, df, verbose=True, allow_dangerous_code=True, handle_parsing_errors=True
    )
    return agent