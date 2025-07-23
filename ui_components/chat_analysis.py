import streamlit as st
import re
import time
import sys
import io
import plotly.graph_objects as go
import plotly.express as px

def render_chat_analysis_tab(messages, agent, df):
    st.subheader("Chat with your data")
    for idx, message in enumerate(messages):
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">'
                       f'<div>👤</div>'
                       f'<div class="message-content">{message["content"]}</div>'
                       f'</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f'<div class="chat-message bot-message">'
                       f'<div>🤖</div>'
                       f'<div class="message-content">{message["content"]}</div>'
                       f'</div>', unsafe_allow_html=True)
        elif message["role"] == "plot":
            st.plotly_chart(message["content"], key=f"plotly_{idx}")
    with st.container():
        if prompt := st.chat_input("Ask a question about your data..."):
            messages.append({
                "role": "user",
                "content": prompt
            })
            st.markdown(f'<div class="chat-message user-message">'
                       f'<div>👤</div>'
                       f'<div class="message-content">{prompt}</div>'
                       f'</div>', unsafe_allow_html=True)
            with st.status("Processing your question...", expanded=True) as status:
                st.write("Analyzing data and generating response...")
                SYSTEM_PROMPT = (
                    """
                    You are a data assistant. The user has uploaded a CSV file, and the entire contents are loaded into a pandas DataFrame named 'df'.
                    - You must ALWAYS use the provided DataFrame 'df' for ALL analysis, calculations, and plotting.
                    - NEVER create, use, or reference any sample, synthetic, or hardcoded data. Do not create your own DataFrame or data dictionary.
                    - If the user asks for a plot, chart, graph, or visualization, respond ONLY with a Python code block ```python...``` (using plotly.express as px or plotly.graph_objects as go) that creates the plot, and assign the figure to a variable named 'fig'.
                    - Do NOT use fig.show() or fig.show_plotly() in python code block.
                    - Do NOT use matplotlib or seaborn.
                    - Do NOT create or overwrite the DataFrame. Only use the provided 'df'.
                    - If the user asks a question that does NOT require a plot, respond with a concise English answer and do NOT return any code.
                    - If the user asks a question that is not related to the data, respond with a concise English answer to stay on the topic of the data.
                    """
                )
                full_prompt = f"{SYSTEM_PROMPT}\n{prompt}"
                try:
                    response = agent.run(full_prompt)
                    time.sleep(0.5)
                    response_str = str(response)
                    code_block = re.search(r"```python(.*?)```", response_str, re.DOTALL)
                    if not code_block:
                        code_block = re.search(r"```(.*?)```", response_str, re.DOTALL)
                    if not code_block and "Final Answer:" in response_str:
                        final_answer = response_str.split("Final Answer:")[-1].strip()
                        # Try to extract code from backticks first
                        code_in_ticks = re.search(r"`([^`]+)`", final_answer)
                        if code_in_ticks:
                            code = code_in_ticks.group(1)
                        else:
                            # Try to extract code after 'is', 'as follows:', or ':'
                            code = final_answer
                            for sep in ["is", "as follows:", ":"]:
                                if sep in code:
                                    code = code.split(sep, 1)[-1].strip()
                        code = code.strip("` \n")
                        if code:
                            code_block = type('obj', (object,), {'group': lambda self, x: code})()
                    # NEW: Try to detect and execute code if it looks like Python code (e.g., starts with 'import' and contains 'fig =')
                    if not code_block and response_str.strip().startswith('import') and 'fig =' in response_str:
                        code = response_str.strip()
                        code_block = type('obj', (object,), {'group': lambda self, x: code})()
                    if code_block:
                        code = code_block.group(1)
                        code = re.sub(r'\\.show\\s*\\(\\s*\\)', '', code)
                        local_vars = {'df': df, 'go': go, 'px': px}
                        global_vars = {}
                        fig = None
                        old_stdout = sys.stdout
                        sys.stdout = mystdout = io.StringIO()
                        try:
                            exec(code, global_vars, local_vars)
                            fig = local_vars.get('fig', None)
                            if fig is not None:
                                messages.append({"role": "plot", "content": fig})
                            else:
                                # If code executed but no fig, show code as text
                                messages.append({"role": "assistant", "content": f"Code executed but no plot was produced. Here is the code:\n\n```python\n{code}\n```"})
                        except Exception as e:
                            st.error(f"Error executing visualization code: {e}")
                            messages.append({"role": "assistant", "content": f"Error executing code: {e}\n\nCode:\n```python\n{code}\n```"})
                        finally:
                            sys.stdout = old_stdout
                    else:
                        messages.append({"role": "assistant", "content": str(response)})
                    status.update(label="Complete!", state="complete")
                except ValueError as e:
                    if 'output parsing error' in str(e).lower():
                        messages.append({
                            "role": "assistant",
                            "content": "Sorry, I couldn't understand the response from the language model. Please try rephrasing your question or ask something else."
                        })
                    else:
                        messages.append({
                            "role": "assistant",
                            "content": f"An error occurred: {e}"
                        })
                st.rerun() 