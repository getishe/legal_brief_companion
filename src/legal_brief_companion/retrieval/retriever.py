from langchain_community.vectorstores import Chroma
from legal_brief_companion.config.settings import settings
from langchain_huggingface import HuggingFaceEmbeddings

def get_retriever(filters: dict = None, max_chunks: int = 4):
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu",
            "trust_remote_code": True
        }
    )

    
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=str(settings.VECTOR_STORE_PATH),
        collection_name="legal_briefs"
    )

    search_kwargs = {"k": max_chunks}
    if filters:
        search_kwargs["filter"] = {"where": filters}

    return vector_store.as_retriever(search_kwargs=search_kwargs)




