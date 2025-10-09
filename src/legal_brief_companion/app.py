import streamlit as st
from src.legal_brief_companion.llm.chain import build_chain
from legal_brief_companion.config.settings import settings



if __name__ == "__main__":
  st.set_page_config(page_title="Legal Brief Companion", layout="wide")
  st.title("⚖️ Legal Brief Companion")
  
  #Dropdown to select model
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
    chain = build_chain(query_type, filters=filters)

    try:
      
        chain, docs = build_chain(query_type="summary", filters=filters)
        output = chain.invoke({"query": query})
        response = output["result"]
        docs = output["source_documents"]

        st.write("🧠 Response:", response)
        
        # ✅ Page-level citations
          #  with st.expander("📄 Sources"):
        if docs:
            st.markdown("### 📄 Sources with Page References")
            for doc in docs:
                page = doc.metadata.get("page_label", doc.metadata.get("page"))
                st.markdown(f"- `{doc.metadata['source']}`, page {page}")
        else:
                st.warning("No source documents found for this query.")
         # Show unique sources used
        if docs:
          unique_sources = sorted(set(doc.metadata["source"] for doc in docs))
          st.markdown("### 📄 Sources")
          for src in unique_sources:
             st.markdown(f"- `{src}`")
        else:
           st.warning("No sources found for this query.")

          
          
               # response = chain.invoke({"query": query})
        # print(f"🧠 Chain response: {response}")
        # st.markdown(f"### Response\n{response['result']}")
        
        # if "source_documents" in response:
        #     st.markdown("### 📄 Sources")
        #     for doc in response["source_documents"]:
        #         st.markdown(f"- {doc.metadata.get('source', 'Unknown source')}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

        #   for doc in response["source_documents"]:
        #         st.markdown(f"- {doc.metadata['source']}")
        #         st.markdown(f"  - {doc.page_content[:max_chars]}...")
        #         st.markdown(f"  - (Score: {doc.metadata.get('score', 'N/A')})")
        #         st.markdown("---")
                
  
  
    