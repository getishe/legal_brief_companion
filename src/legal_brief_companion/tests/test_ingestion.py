from langchain_core.documents import Document

from ingestion.text_splitter import split_documents


def test_split_documents_preserves_metadata():
    documents = [
        Document(
            page_content="A" * 700,
            metadata={"source": "case.pdf", "case": "Example Case"},
        )
    ]

    chunks = split_documents(documents, chunks_size=300, chunk_overlap=30)

    assert len(chunks) > 1
    assert all(chunk.metadata["source"] == "case.pdf" for chunk in chunks)
    assert all(chunk.metadata["case"] == "Example Case" for chunk in chunks)
