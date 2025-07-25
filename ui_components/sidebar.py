import streamlit as st
import os
import pandas as pd

def sidebar():
    with st.sidebar:
        st.markdown("# Settings")
        st.markdown("---")
        st.session_state.llm_type = st.radio(
            "Select LLM Provider",
            ["openai", "gemini", "groq"],
            index=["openai", "gemini", "groq"].index(st.session_state.llm_type) if st.session_state.llm_type in ["openai", "gemini", "groq"] else 0
        )

        # --- API Key UX ---
        llm_type = st.session_state.llm_type
        key_label = {
            "openai": "OpenAI API Key",
            "gemini": "Gemini API Key",
            "groq": "Groq API Key"
        }[llm_type]
        help_links = {
            "openai": "Get your key [here](https://platform.openai.com/account/api-keys)",
            "gemini": "Get your key [here](https://aistudio.google.com/app/apikey)",
            "groq": "Get your key [here](https://console.groq.com/keys)"
        }
        env_var = {
            "openai": "OPENAI_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "groq": "GROQ_API_KEY"
        }[llm_type]
        default_key = os.getenv(env_var, "")
        key_state_name = f"{llm_type}_api_key"
        key_value = st.session_state.get(key_state_name, default_key)

        # On first load, show info about API key privacy
        if "api_key_info_shown" not in st.session_state:
            st.info("""
            **API Key Privacy**  
            Your API key is only used in your browser session and never sent to any server except the LLM provider.  
            You can get a free or paid API key from the provider's website.  
            """, icon="🔒")
            st.session_state.api_key_info_shown = True

        # Masked display and change logic
        if key_value and not st.session_state.get(f"show_{key_state_name}_input", False):
            masked = key_value[:4] + "..." + key_value[-4:] if len(key_value) > 8 else "****"
            st.success(f"{key_label} set! :white_check_mark:  ")
            st.write(f"**Current Key:** `{masked}`")
            if st.button(f"Change {key_label}"):
                st.session_state[f"show_{key_state_name}_input"] = True
        else:
            if not key_value:
                st.warning(f"{key_label} required :warning:")
            st.session_state[key_state_name] = st.text_input(
                key_label,
                value=key_value,
                type="password",
                help=f"Enter your {llm_type.capitalize()} API key. {help_links[llm_type]}"
            )
            if st.session_state.get(f"show_{key_state_name}_input", False):
                if st.button(f"Done Editing {key_label}"):
                    st.session_state[f"show_{key_state_name}_input"] = False

        # Session info
        with st.expander("Session Info"):
            if not st.session_state.df.empty:
                st.write(f"Rows: {len(st.session_state.df)}")
                st.write(f"Columns: {len(st.session_state.df.columns)}")
                st.write(f"File: {st.session_state.filename}")
            else:
                st.write("No data loaded")
        # Clear data button
        if not st.session_state.df.empty:
            if st.button("Clear Data"):
                st.session_state.df = pd.DataFrame()
                st.session_state.filename = None
                st.session_state.messages = []
                st.session_state.agent = None
                st.rerun()
        # KPIs (if data loaded)
        if not st.session_state.df.empty:
            df = st.session_state.df
            st.header("Dataset KPIs")
            st.metric("Rows", df.shape[0])
            st.metric("Columns", df.shape[1])
            num_missing = df.isnull().sum().sum()
            percent_missing = (num_missing / (df.shape[0] * df.shape[1])) * 100 if df.size > 0 else 0
            st.metric("Missing Values", num_missing)
            st.metric("Missing (%)", f"{percent_missing:.2f}%")
            st.metric("Duplicate Rows", df.duplicated().sum())
            st.write("**Numeric Summary:**")
            st.dataframe(df.describe())
            st.write("**Non-Numeric Columns:**")
            non_numeric_cols = df.select_dtypes(exclude='number').columns
            if len(non_numeric_cols) > 0:
                nunique = df[non_numeric_cols].nunique().to_frame("Unique Values")
                st.dataframe(nunique)
            else:
                st.write("No non-numeric columns.")

        # Reset Session Button
        if st.button("Reset Session"):
            for k in [
                "df", "filename", "messages", "agent",
                "openai_api_key", "gemini_api_key", "groq_api_key",
                "show_openai_api_key_input", "show_gemini_api_key_input", "show_groq_api_key_input",
                "api_key_info_shown"
            ]:
                st.session_state.pop(k, None)
            st.rerun()