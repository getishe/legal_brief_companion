from langchain.chains import retrieval_qa
from langchain_groq import ChatGroq
from src.llm.prompt_templates import get_prompt_template
from src.retrieval.retriever import get_retriever

def build_chain(query_type: str):
    retriever = get_retriever()
    prompt_template = get_prompt_template(query_type)
    llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
    # other params...
)
    chain = retrieval_qa.RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )
    return chain