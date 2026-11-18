import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st

if hasattr(st, "secrets"):
    for secret_name in ("GROQ_API_KEY", "EMBEDDING_MODEL", "LLM_MODEL"):
        if secret_name not in os.environ:
            secret_value = st.secrets.get(secret_name)
            if secret_value:
                os.environ[secret_name] = str(secret_value)

from legal_brief_companion.config.settings import settings
from legal_brief_companion.llm.chain import build_chain


def main():
    st.set_page_config(page_title="Legal Brief Companion", layout="wide")
    st.title("⚖️ Legal Brief Companion")
    st.caption(
        "Research assistance only. Verify authorities, citations, and advice with a qualified attorney."
    )

    api_key_configured = settings.GROQ_API_KEY not in ("demo-key", None, "")
    if not api_key_configured:
        st.error(
            "GROQ_API_KEY is not configured. Set it in your environment or Streamlit secrets."
        )

    case = st.selectbox(
        "Choose a case",
        ["Tinker v. Des Moines"],
    )
    jurisdiction = st.selectbox(
        "Jurisdiction",
        ["8th Circuit"],
    )
    model = st.selectbox(
        "Model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
    )
    query_type = st.selectbox(
        "Query type",
        ["question", "summary", "argument", "citation"],
    )

    query = st.text_area("Enter your legal question", height=120)
    show_resources = st.checkbox("Show resources used")
    max_chars = st.slider(
        "Max response length",
        min_value=100,
        max_value=2000,
        value=500,
        step=100,
    )

    if st.button("Submit"):
        if not api_key_configured:
            st.stop()
        if not query.strip():
            st.warning("Enter a legal question before submitting.")
            st.stop()

        settings.LLM_MODEL = model
        filters = {"case": case}
        if jurisdiction != "Federal District":
            filters["jurisdiction"] = jurisdiction

        try:
            chain = build_chain(
                query_type,
                filters=filters,
                max_chunks=4,
                max_tokens=max(64, max_chars // 4),
            )
            with st.spinner("Generating a sourced response..."):
                output = chain.invoke({"query": query})
                response = output["result"]
                docs = output.get("source_documents", [])

            st.success("Response generated.")
            st.write("**Answer:**", response)

            if show_resources and docs:
                st.markdown("### 📄 Sources with Page References")
                for index, doc in enumerate(docs, 1):
                    source = doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get(
                        "page_label",
                        doc.metadata.get("page", "N/A"),
                    )
                    case_name = doc.metadata.get("case", "Unknown case")
                    with st.expander(
                        f"{index}. {case_name} - page {page}",
                        expanded=False,
                    ):
                        st.markdown(f"**Source:** `{source}`")
                        st.write(doc.page_content)
            elif show_resources:
                st.warning("No source documents found for this query.")

        except Exception as exc:
            st.error("The response could not be generated.")
            if settings.debug:
                st.exception(exc)


if __name__ == "__main__":
    main()
