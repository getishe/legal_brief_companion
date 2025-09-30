from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from config.settings import settings


def build_vector_store(documents):
    """Builds a Chroma vector store from the provided documents."""
    embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
    
    vector_store = Chroma.from_documents(
        documents,
        embeddings=embeddings,
        persist_directory=str(settings.VECTOR_STORE_PATH)
    )
    if vector_store.persist():
        print(f"Vector store persisted at {settings.VECTOR_STORE_PATH}.")
    print(f"Vector store created at {len(documents)} documents.")
    return vector_store