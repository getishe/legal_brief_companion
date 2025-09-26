import os 
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

#Path 
from pathlib import Path
from config.settings import Settings
DOCUMENT_DIR = Path(os.getenv("DOCUMENT_DIR", "data/Tinker v. Des Moines (8th Cir.).pdf"))
# Path to store processed documents
# Path to store processed documents
VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH", "data/vector_store"))
# Access the database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/knowledge_base.db")

# MODEL SETTINGS
class Settings:
    DOCUMENT_DIR = Path(os.getenv("DOCUMENT_DIR", "data/Tinker v. Des Moines (8th Cir.).pdf"))
    VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH", "data/vector_store"))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/knowledge_base.db")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

print(Settings.DOCUMENT_DIR)
print(Settings.VECTOR_STORE_PATH)
print(Settings.DATABASE_URL)
print(Settings.GROQ_API_KEY)
print(Settings.EMBEDDING_MODEL)
print(Settings.LLM_MODEL)

if not Settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from environment variables.")

