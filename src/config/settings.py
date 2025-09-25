import os 
from dotenv import load_dotenv

load_dotenv()

#Path 

DOCUMENT_DIR = os.getenv("DOCUMENT_DIR", "data/documents")
# Path to store processed documents
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/vector_store")


# MODEL SETTINGS
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")