import streamlit as st
def sidebar():
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("# Settings")
        st.markdown("---")
        st.session_state.llm_type = st.radio(
            "Select LLM Provider",
            ["openai", "gemini", "groq"],
            index=["openai", "gemini", "groq"].index(st.session_state.llm_type) if st.session_state.llm_type in ["openai", "gemini", "groq"] else 0
        )
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
            st.write(df.describe())
            st.write("**Non-Numeric Columns:**")
            non_numeric_cols = df.select_dtypes(exclude='number').columns
            if len(non_numeric_cols) > 0:
                nunique = df[non_numeric_cols].nunique().to_frame("Unique Values")
                st.write(nunique)
            else:
                st.write("No non-numeric columns.")