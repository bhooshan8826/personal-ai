"""
Application configuration management
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # App
    app_name: str = "Personal AI Assistant"
    app_env: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    encryption_key: str = os.getenv("ENCRYPTION_KEY", "dev-encryption-key-32-chars-minimum!!")

    # LLM Configuration
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

    # API
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/app.log")

    # Vector DB
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "data/vector_db")
    chroma_host: str = os.getenv("CHROMA_HOST", "localhost")
    chroma_port: int = int(os.getenv("CHROMA_PORT", "8001"))

    # Optional: Claude API
    claude_api_key: str = os.getenv("CLAUDE_API_KEY", "")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()


# Export settings instance
settings = get_settings()
