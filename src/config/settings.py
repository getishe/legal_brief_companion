from pathlib import Path
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    DOCUMENT_DIR: Path = Path("data/Tinker v. Des Moines (8th Cir.).pdf")
    VECTOR_STORE_PATH: Path = Path("data/vector_store")
    DATABASE_URL: str = "sqlite:///data/knowledge_base.db"
    
    GROQ_API_KEY: str
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate settings
settings = Settings()

# Optional: Debug print
if __name__ == "__main__":
    print("📁 Document Path:", settings.DOCUMENT_DIR)
    print("📦 Vector Store Path:", settings.VECTOR_STORE_PATH)
    print("🗄️ Database URL:", settings.DATABASE_URL)
    print("🔑 GROQ API Key:", settings.GROQ_API_KEY)
    print("🧠 Embedding Model:", settings.EMBEDDING_MODEL)
    print("🤖 LLM Model:", settings.LLM_MODEL)

    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing from environment variables.")
