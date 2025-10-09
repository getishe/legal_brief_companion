from pathlib import Path
from pydantic_settings import BaseSettings
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: str
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_PROVIDER: str = "groq"
    DATABASE_URL: str = "sqlite:///data/knowledge_base.db"
    LLM_MODEL: str = "llama-3.1-8b-instant"
    
    API_KEY: Optional[str] = None
    MODEL_NAME: Optional[str] = None
    VECTOR_STORE_TYPE: Optional[str] = None
    DOCUMENTS_PATH: str = "data/documents"
    PERSIST_DIRECTORY: str = "data/vector_store"
    debug: bool = False

    @property
    def PERSIST_DIR(self) -> Path:
        return Path(self.PERSIST_DIRECTORY)

    @property
    def DOCUMENT_DIR(self) -> Path:
        return Path(self.DOCUMENTS_PATH)

    @property
    def VECTOR_STORE_PATH(self) -> Path:
        return Path("data/vector_store")

    def get_embedding_model(self):
        return HuggingFaceEmbeddings(model_name=self.EMBEDDING_MODEL)

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
