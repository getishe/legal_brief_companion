from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from legal_brief_companion.config.settings import settings

def build_vector_store(documents):
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu", "trust_remote_code": True}
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(settings.VECTOR_STORE_PATH),
        collection_name="legal_briefs"
    )

    print(f"✅ Vector store persisted at: {settings.VECTOR_STORE_PATH}")



