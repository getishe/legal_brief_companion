from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
from config.settings import settings
from langchain_huggingface import HuggingFaceEmbeddings
def build_vector_store(documents):
    """Builds a Chroma vector store from the provided documents."""
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

    vector_store = Chroma.from_documents(
        documents,
        embedding=embeddings,
        persist_directory=str(settings.VECTOR_STORE_PATH)
    )

    # Persist the store
    vector_store.persist()

    # Confirmation prints
    print(f"✅ Vector store persisted at: {settings.VECTOR_STORE_PATH}")
    print(f"📄 Documents embedded: {len(documents)}")
    print("📦 Vector store build complete.")

    return vector_store
