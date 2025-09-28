from langchain.vectorstores import Chroma 
from config.settings import settings 

def query_vector_store():
    """
    Loads the persistent vector store and returns a retriever object.
    """
    vector_store = Chroma(
        persist_directory=str(settings.VECTOR_STORE_PATH),
        embedding_function=None
    )
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    print("🔍 Retriever loaded with top-k = 3")
    return retriever
