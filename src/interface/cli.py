import json
import typer
from ingestion.document_loader import load_documents
from ingestion.text_splitter import split_documents 
from retrieval.vector_store import build_vector_store
from llm.chain import build_chain
from config import settings
from typing import Optional
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
def query(
    query: str,
    query_type: str = "default",
    fast: bool = False,
    show_sources: bool = False,
    max_chars: int = 300,
    format: str = "text",
    filter: Optional[str] = None  
):
    filters = None
    if filter:
      try:
          filters = json.loads(filter)
      except json.JSONDecodeError:
          print("❌ Invalid filter format. Use JSON like: '{\"year\": 1969}'")
          return

    """
    Ask a question using the RAG assistant.
    Use --fast for quicker responses.
    Use --show-sources to display retrieved documents.
    """
    filters = {"year": 1969} if "Tinker" in query else None

    if fast:
        settings.LLM_MODEL = "llama-3.1-8b-instant"
        chain = build_chain(query_type, filters=filters, max_chunks=2)
    else:
        chain = build_chain(query_type, filters=filters)

    response = chain.invoke({"query": query})
    print(f"🤖 Response:\n{response['result']}\n")

    #how sources if flag is set
    if show_sources:
        for i, doc in enumerate(response.get("source_documents", []), 1):
            print(f"📄 Source {i}: {doc.metadata.get('source', 'Unknown')}")
            print(doc.page_content[:max_chars])

  # Print first 500 chars







# ✅ This must be outside all functions
if __name__ == "__main__":
    app()
