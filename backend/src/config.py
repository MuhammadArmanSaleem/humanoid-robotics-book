from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Gemini API settings
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"

    # Qdrant settings
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "textbook_content"

    # Database settings
    database_url: str
    jwt_secret_key: str
    jwt_expiration_days: int = 7
    bcrypt_rounds: int = 12

    # Auth0 settings (for future SSO integration)
    auth0_domain: Optional[str] = None
    auth0_client_id: Optional[str] = None
    auth0_client_secret: Optional[str] = None
    auth0_audience: Optional[str] = None

    # Frontend settings
    frontend_url: str = "http://localhost:3000"

    # Server settings
    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8000

    # Session settings
    session_timeout_hours: int = 24

    # Content settings
    content_chunk_size: int = 500  # words
    content_overlap_size: int = 50  # words

    # RAG settings
    rag_top_k: int = 5
    rag_min_relevance_score: float = 0.3

    class Config:
        env_file = ".env.local"  # Use .env.local as specified
        case_sensitive = False


# Create a global settings instance
settings = Settings()