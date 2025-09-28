from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from config.settings import settings

def load_documents():
    documents = []
    doc_path = settings.DOCUMENT_DIR
    
    # If it's a directory, iterate through files
    if doc_path.is_dir():
        for file in doc_path.iterdir():
            if file.suffix == '.txt':
                loader = TextLoader(str(file), encoding='utf-8')
                documents.extend(loader.load())
            elif file.suffix == '.pdf':
                loader = PyPDFLoader(str(file))
                documents.extend(loader.load())
            
                # Skip unsupported file types in directory   
            elif doc_path.is_file():
                if doc_path.suffix == ".txt":
                        loader = TextLoader(str(doc_path), encoding="utf-8")
                        documents.extend(loader.load())
            elif doc_path.suffix == ".pdf":
                  loader = PyPDFLoader(str(doc_path))
                  documents.extend(loader.load())
        else:
            raise ValueError("Unsupported file type. Only .txt and .pdf are supported.")
    else:
        raise ValueError(f"DOCUMENT_DIR must be a valid file or directory path.")
    print(f"Loaded {len(documents)} documents from {doc_path}")
    return documents


# import os

# class DocumentLoader:
#     def __init__(self, source_directory):
#         self.source_directory = source_directory

#     def load_documents(self):
#         documents = []
#         for filename in os.listdir(self.source_directory):
#             if filename.endswith('.txt'):
#                 with open(os.path.join(self.source_directory, filename), 'r', encoding='utf-8') as file:
#                     documents.append(file.read())
#         return documents