import os 
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from config.settings import DOCUMENT_DIR

def load_documents():
    documents = []
    for filename in os.listdir(DOCUMENT_DIR):
        if filename.endswith('.txt') or filename.endswith('.pdf'):
            loader = TextLoader(os.path.join(DOCUMENT_DIR, filename), encoding='utf-8')
            documents.extend(loader.load())
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