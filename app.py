import streamlit as st

st.title("Legal Brief Companion")
query = st.text_input("Ask a legal question:")
if query:
    st.write(f"You asked: {query}") # Placeholder for LLM response
