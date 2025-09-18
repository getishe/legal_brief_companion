from src.loaders.pdf_loader import load_pdf
from src.processing.chunker import chunk_text
from src.embeddings.embedder import embed_chunks
from src.embeddings.vector_store import save_vectorstore

docs = load_pdf("data/raw/brief.pdf")
chunks = chunk_text(docs)
vectorstore = embed_chunks(chunks)
save_vectorstore(vectorstore, "outputs/vectorstore/index.faiss")
