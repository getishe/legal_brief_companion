from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from legal_brief_companion.config.settings import settings
def load_documents():
    documents = []
    doc_path = settings.DOCUMENT_DIR
    known_metadata = {
        "Tinker v. Des Moines": {
            "jurisdiction": "8th Circuit",
            "case": "Tinker v. Des Moines",
            "year": 1969,
        }
    }

    def add_metadata(docs, file):
        name = file.stem
        metadata = (
            known_metadata["Tinker v. Des Moines"]
            if "Tinker v. Des Moines" in name
            else {}
        )
        for doc in docs:
            doc.metadata.update({
                "source": str(file),
                "jurisdiction": metadata.get("jurisdiction", "Not specified"),
                "case": metadata.get("case", name),
                "year": metadata.get("year"),
            })
            documents.append(doc)

    if doc_path.is_dir():
        for file in doc_path.iterdir():
            if file.suffix.lower() == ".txt":
                print(f"📄 Loading TXT: {file.name}")
                loader = TextLoader(str(file), encoding="utf-8")
                docs = loader.load()
            elif file.suffix.lower() == ".pdf":
                print(f"📄 Loading PDF: {file.name}")
                loader = PyPDFLoader(str(file))
                docs = loader.load()
            else:
                print(f"⚠️ Skipping unsupported file: {file.name}")
                continue

            add_metadata(docs, file)

    elif doc_path.is_file():
        if doc_path.suffix.lower() == ".txt":
            print(f"📄 Loading single TXT file: {doc_path.name}")
            loader = TextLoader(str(doc_path), encoding="utf-8")
            docs = loader.load()
        elif doc_path.suffix.lower() == ".pdf":
            print(f"📄 Loading single PDF file: {doc_path.name}")
            loader = PyPDFLoader(str(doc_path))
            docs = loader.load()
        else:
            raise ValueError("Unsupported file type. Only .txt and .pdf are supported.")

        add_metadata(docs, doc_path)

    else:
        raise ValueError(f"DOCUMENT_DIR must be a valid file or directory path. Got: {doc_path}")

    print(f"✅ Loaded {len(documents)} documents from {doc_path}")
    return documents
