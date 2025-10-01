# from langchain.chains import retrieval_qa
# from langchain_groq import ChatGroq
# from src.llm.prompt_templates import get_prompt_template
# from src.retrieval.retriever import get_retriever

# def build_chain(query_type: str, chain_type: str= "stuff"):
#     retriever = get_retriever()
#     prompt_template = get_prompt_template(query_type)
#     llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0.0,
#     max_retries=2,
#     # other params...
# )
#     chain = retrieval_qa.RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type=chain_type,
#         retriever=retriever,
#         return_source_documents=True,
#         chain_type_kwargs={"prompt": prompt_template}
#     )
    
#     print(f"🔗 Chain built with model: {llm.model}, prompt type: {query_type}")
      
#     return chain
# poetry run python src/interface/cli.py ingest
# poetry run python src/interface/cli.py query "What is the precedent in Tinker v. Des Moines?" --query-type question

from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from config.settings import settings
from src.llm.prompt_templates import get_prompt_template
from src.retrieval.retriever import get_retriever

def build_chain(query_type: str, chain_type: str = "stuff"):
    retriever = get_retriever()  # ✅ Define retriever first
    prompt_template = get_prompt_template(query_type)

    # ✅ Diagnostic: test retrieval
    test_query = "What is the precedent in Tinker v. Des Moines?"
    docs = retriever.invoke(test_query)
    print(f"📄 Retrieved {len(docs)} documents for test query.")
    for i, doc in enumerate(docs, 1):
        print(f"\n--- Doc {i} ---\n{doc.page_content[:300]}")

    # Dynamically select model from settings
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.0,
        max_retries=2,
        groq_api_key=settings.GROQ_API_KEY
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )

    print(f"🔗 Chain built with model: {settings.LLM_MODEL}, prompt type: {query_type}")
    return chain

# https://copilot.microsoft.com/shares/SG7eXKsW3ckeKKLeaBkog
# https://copilot.microsoft.com/shares/tKD9UVJqLRdAKeqvmK3FZ
# https://copilot.microsoft.com/shares/tKD9UVJqLRdAKeqvmK3FZ