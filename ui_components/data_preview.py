import streamlit as st
import pandas as pd

def render_data_preview_tab(df, filename):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Preview: {filename}")
        st.write("\n\n")
        st.dataframe(df.head(100), use_container_width=True)
    with col2:
        st.subheader(f"Column Info:")
        st.write("\n\n")
        column_info = pd.DataFrame({
            'Column': list(df.columns),
            'Type': df.dtypes.astype(str).values,
            'Unique Values': [df[col].nunique() for col in df.columns],
            'Missing Values': [df[col].isna().sum() for col in df.columns]
        })
        st.dataframe(column_info, use_container_width=True) 