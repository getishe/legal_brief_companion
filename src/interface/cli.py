import typer
from ingestion.document_loader import load_documents
from ingestion.text_splitter import split_documents 
from retrieval.vector_store import build_vector_store
from llm.chain import build_chain

app = typer.Typer()

@app.command()
def ingest():
    """
    Load, split, and embed documents into the vector store.
    """
    docs = load_documents()
    print(f"📄 Loaded {len(docs)} documents.")
    chunks = split_documents(docs)
    print(f"✂️ Split into {len(chunks)} chunks.")
   
    try:
        build_vector_store(chunks)
        print("📦 Vector store built successfully.")
    except Exception as e:
        print(f"❌ Error during vector store build: {type(e).__name__} - {e}")
        raise  # Optional: re-raise to preserve traceback

    print("📚 Ingestion complete.")

@app.command()
def query(query: str, query_type: str = "default"):
    """
    Ask a question using the RAG assistant.
    """
    chain = build_chain(query_type)
    response = chain.run(query)
    print(f"🤖 Response:\n{response}")

# ✅ This must be outside all functions
if __name__ == "__main__":
    app()
