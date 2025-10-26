import sys
import os

# ✅ Ensure src/ is on the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from legal_brief_companion.llm.chain import build_chain
from legal_brief_companion.config.settings import settings

if settings.debug:
   if settings.GROQ_API_KEY in ("demo-key", None, ""):  
     st.warning("⚠️ No valid GROQ_API_KEY found. Please set it in Streamlit Secrets.")   
else: 
   st.success("GroQ_API_KEY loaded successfully.")     
      
def main():
    st.set_page_config(page_title="Legal Brief Companion", layout="wide")
    st.title("⚖️ Legal Brief Companion")

    # Dropdowns
    case = st.selectbox("Choose a case", ["Tinker v. Des Moines", "Brown v. Board", "Roe v. Wade", "Miranda v. Arizona"])
    jurisdiction = st.selectbox("Jurisdiction", ["8th Circuit", "Supreme Court", "Federal District"])
    model = st.selectbox("Model", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])
    query_type = st.selectbox("Query type", ["question", "summary", "argument"])

    query = st.text_area("Enter your legal question", height=100)
    show_resources = st.checkbox("Show resources used")
    max_chars = st.slider("Max response length", min_value=100, max_value=2000, value=500, step=100)

    if st.button("Submit"):
        settings.LLM_MODEL = model
        filters = None
        chain, docs = build_chain(query_type, filters=filters)
        
        try:
          with st.spinner("🤖 Thinking... Generating response..."):
            output = chain.invoke({"query": query})
            response = output["result"]
            docs = output.get("source_documents", [])

          st.success("✅ Response generated successfully!")
          st.write("🧠 **Answer:**", response)

            # Show resources if available
          if show_resources and docs:
                st.markdown("### 📄 Sources with Page References")
                for doc in docs:
                    source = doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get("page_label", doc.metadata.get("page", "N/A"))
                    st.markdown(f"- `{source}`, page {page}")
          elif show_resources:
                st.warning("No source documents found for this query.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
