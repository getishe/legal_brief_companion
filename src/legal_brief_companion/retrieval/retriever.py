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




# def get_retriever(filters: dict = None, max_chunks: int = 4):
#     embeddings = HuggingFaceEmbeddings(
#         model_name=settings.EMBEDDING_MODEL,
#         model_kwargs={"device": "cpu"}
#     )

#     chroma_settings = Settings(
#         chroma_db_impl="duckdb+parquet",
#         persist_directory=str(settings.VECTOR_STORE_PATH),
#         anonymized_telemetry=False
#     )

#     vector_store = Chroma(
#         embedding_function=embeddings,
#         persist_directory=str(settings.VECTOR_STORE_PATH),
#         client_settings=chroma_settings  # 👈 Explicitly pass settings
#     )

#     return vector_store.as_retriever(search_kwargs={
#         "filter": filters or {},
#         "k": max_chunks
#     })






# from langchain_community.vectorstores import Chroma
# # from langchain_chroma import Chroma
# from legal_brief_companion.config.settings import settings
# from langchain_huggingface import HuggingFaceEmbeddings
# def get_retriever(filters: dict = None, max_chunks: int = 4):
#     embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL, model_kwargs={"device": "cpu"})
#     vector_store = Chroma(
#         embedding_function=embeddings,
#         persist_directory=str(settings.VECTOR_STORE_PATH)
#     )
#     return vector_store.as_retriever(search_kwargs={
#         "filter": filters or {},
#         "k": max_chunks
#     })


# def get_retriever():
#     embedding_model = HuggingFaceEmbeddings(model=settings.EMBEDDING_MODEL)
#     vector_store = Chroma(
#         persist_directory=str(settings.VECTOR_STORE_PATH),
#         embedding_function=embedding_model
#     )
#     return vector_store.as_retriever()
