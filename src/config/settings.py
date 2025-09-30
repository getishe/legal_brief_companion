from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Required by your app
    GROQ_API_KEY: str
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-3.5-turbo"
    DATABASE_URL: str = "sqlite:///data/knowledge_base.db"

    # Match .env fields to avoid extra_forbidden errors
    API_KEY: str = ""
    MODEL_NAME: str = ""
    VECTOR_STORE_TYPE: str = ""
    DOCUMENTS_PATH: str = "data/documents"
    PERSIST_DIRECTORY: str = "data/vector_store"
    
    @property
    def PERSIST_DIR(self) -> Path:
        return Path(self.PERSIST_DIRECTORY)
    # Computed paths
    @property
    def DOCUMENT_DIR(self) -> Path:
        return Path(self.DOCUMENTS_PATH)

    @property
    def VECTOR_STORE_PATH(self) -> Path:
        return Path("data/vector_store")

    debug: bool = False

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
