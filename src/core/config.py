"""Application configuration and settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    api_title: str = "Customer Support Email Agent"
    api_version: str = "0.1.0"
    debug: bool = False

    # LLM Configuration (Groq)
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"
    temperature: float = 0.7
    max_tokens: int = 2000

    # LangGraph Configuration
    max_retries: int = 3
    timeout_seconds: int = 60

    # Application Configuration
    log_level: str = "INFO"
    environment: str = "development"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
