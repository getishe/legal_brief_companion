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
def reset():
    """
    Delete the existing vector store to start fresh.
    """
    import shutil
    from config import settings  # Adjust if your settings are elsewhere

    try:
        shutil.rmtree(settings.VECTOR_STORE_PATH, ignore_errors=True)
        print(f"🧹 Vector store at '{settings.VECTOR_STORE_PATH}' has been reset.")
    except Exception as e:
        print(f"❌ Failed to reset vector store: {type(e).__name__} - {e}")

@app.command()
def status():
    """
    Show current vector store status.
    """
    from pathlib import Path
    from config import settings  # Adjust if needed

    vector_path = Path(settings.VECTOR_STORE_PATH)
    if not vector_path.exists():
        print("📦 No vector store found.")
        return

    index_path = vector_path / "index"
    chunk_files = list(index_path.glob("*.bin"))
    print(f"📍 Vector store path: {vector_path}")
    print(f"📄 Chunk count: {len(chunk_files)}")

@app.command()
def query(query: str, query_type: str = "default"):
    """
    Ask a question using the RAG assistant.
    """
    print(f"🔍 Query received: {query}")
    chain = build_chain(query_type)
    print("🔗 Chain built. Invoking...")

    result = chain.invoke(query)
    print(f"\n🧪 Raw result:\n{result}\n")

    if isinstance(result, dict):
      if "result" in result:
        print(f"\n🤖 Response:\n{result['result']}\n")
        print("📄 Retrieved Documents:")
        for i, doc in enumerate(result.get("source_documents", []), 1):
            print(f"\n--- Document {i} ---")
            print(doc.page_content[:500])
      else:
        print(f"⚠️ No 'result' key in response: {result}")
    else:
        print(f"⚠️ Unexpected result type: {type(result)} - {result}")






# ✅ This must be outside all functions
if __name__ == "__main__":
    app()
