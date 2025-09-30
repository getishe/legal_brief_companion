import typer 
from ingestion.document_loader import load_documents
from ingestion.text_splitter import split_documents 
from retrieval.vector_store import build_vector_store
from llm.chain import build_chain

app = typer.Typer()

@app.command()
def ingest():
    """
    Load, split, and embed  documents into the vector store.
    """
    docs = load_documents()
    chunks = split_documents(docs)
    build_vector_store(chunks)
    print("📚 Ingestion complete.")

@app.command()
def query(query: str, query_type:  str = "defult"):
    """
   Ask a questions using the RAG assistant, 
    """
    chain = build_chain(query_type)
    response = chain.run(query)
    print(f"🤖 Response:\n{response}")
    
    if __name__ == "__main__":
        app()   