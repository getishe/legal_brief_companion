from ingestion.document_loader import load_documents
from ingestion.text_splitter import split_documents
from legal_brief_companion.retrieval.vector_store import build_vector_store

if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    build_vector_store(chunks)
