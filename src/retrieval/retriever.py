# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from config.settings import settings
from langchain_huggingface import HuggingFaceEmbeddings
def get_retriever():
    embedding_model = HuggingFaceEmbeddings(model=settings.EMBEDDING_MODEL)
    vector_store = Chroma(
        persist_directory=str(settings.VECTOR_STORE_PATH),
        embedding_function=embedding_model
    )
    return vector_store.as_retriever()
