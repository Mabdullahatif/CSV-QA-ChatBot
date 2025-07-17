import streamlit as st
import pandas as pd
from io import StringIO
from agents import get_dynamic_agent
import plotly.graph_objects as go
import plotly.express as px
import re
import sys
import io
from custom_css.apply_custom_css import apply_custom_css

st.markdown(apply_custom_css(), unsafe_allow_html=True)
st.title("Titanic Project")

SYSTEM_PROMPT = (
    "You are a data assistant. If the user asks for a plot, chart, graph, or visualization, "
    "respond ONLY with a Python code block (using Plotly Express as px or Plotly Graph Objects as go) that creates the plot, "
    "and assign the figure to a variable named 'fig'. Do NOT use matplotlib or seaborn. "
    "If the user asks a question that does NOT require a plot, respond with a concise English answer and do NOT return any code."
    "The DataFrame is named 'df'."
)

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'messages' not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("Upload your csv file", type=["csv"])
llm_type = st.sidebar.selectbox(
    "Choose LLM",
    options=["gemini", "openai"],
    index=0,
    help="Select which LLM to use for Q&A and visualization."
)

if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.session_state.df = pd.read_csv(stringio)
    st.success("File uploaded and DataFrame loaded!")
    st.session_state.agent = get_dynamic_agent(st.session_state.df, llm_type=llm_type)

if not st.session_state.df.empty:
    st.subheader(f"Uploaded DataFrame: {uploaded_file.name if uploaded_file else 'DataFrame'}")
    st.dataframe(st.session_state.df)

def extract_plotly_code(response):
    """Extracts a plotly code block from the LLM response, if present."""
    match = re.search(r"```python(.*?)```", str(response), re.DOTALL)
    if match:
        code = match.group(1)
        # Remove any .show() calls
        code = re.sub(r'\\.show\\s*\\(\\s*\\)', '', code)
        return code.strip()
    return None

def execute_plotly_code(code, df):
    """Executes plotly code in a restricted namespace and returns the figure."""
    local_vars = {'df': df, 'go': go, 'px': px}
    global_vars = {}
    fig = None
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        exec(code, global_vars, local_vars)
        fig = local_vars.get('fig', None)
    except Exception as e:
        st.error(f"Error executing visualization code: {e}")
    finally:
        sys.stdout = old_stdout
    return fig

if prompt := st.chat_input("Ask a question about the data..."):
    if 'agent' in st.session_state:
        full_prompt = f"{SYSTEM_PROMPT}\n{prompt}"
        response = st.session_state.agent.run(full_prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        code_block = extract_plotly_code(response)
        if code_block:
            fig = execute_plotly_code(code_block, st.session_state.df)
            if fig is not None:
                st.session_state.messages.append({"role": "plot", "content": fig})
        else:
            st.session_state.messages.append({"role": "assistant", "content": str(response)})
    else:
        st.warning("Please upload a CSV file first.")

# Display messages in order
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""<div class="row user-message chat-bubble">
            <div style="margin-right: 10px; text-align: right;">{msg['content']}</div>
            <img src="https://cdn-icons-png.flaticon.com/512/149/149072.png" class="avatar" />
        </div>""", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"""<div class="row assistant-message chat-bubble">
            <img src="https://cdn-icons-png.flaticon.com/512/149/149074.png" class="avatar" />
            <div style="margin-left: 10px;">{msg['content']}</div>
        </div>""", unsafe_allow_html=True)
    elif msg["role"] == "plot":
        st.plotly_chart(msg["content"])