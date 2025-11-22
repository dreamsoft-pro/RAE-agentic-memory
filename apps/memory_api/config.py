from pydantic_settings import BaseSettings
from pydantic import model_validator, ConfigDict
import os

class Settings(BaseSettings):
    """
    Configuration settings for the Memory API service.
    Settings are loaded from environment variables and/or a .env file.
    """
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "memory"
    POSTGRES_USER: str = "memory"
    POSTGRES_PASSWORD: str = "example"

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    RERANKER_API_URL: str = "http://localhost:8001"
    MEMORY_API_URL: str = "http://localhost:8000"

    LLM_MODEL: str | None = None
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    OLLAMA_API_URL: str = "http://localhost:11434"
    RAE_LLM_BACKEND: str = "ollama"
    RAE_LLM_MODEL_DEFAULT: str = "llama3"
    EXTRACTION_MODEL: str = "gpt-4o-mini"
    SYNTHESIS_MODEL: str = "gpt-4o"
    RAE_VECTOR_BACKEND: str = "qdrant"
    ONNX_EMBEDDER_PATH: str | None = None

    @model_validator(mode='after')
    def validate_vector_backend(self):
        """Backward compatibility: Support legacy VECTOR_STORE_BACKEND variable"""
        if os.getenv('VECTOR_STORE_BACKEND') and not os.getenv('RAE_VECTOR_BACKEND'):
            self.RAE_VECTOR_BACKEND = os.getenv('VECTOR_STORE_BACKEND')
        return self
    
    # --- Security Settings ---
    OAUTH_ENABLED: bool = True
    OAUTH_DOMAIN: str = "" # e.g., "your-tenant.us.auth0.com"
    OAUTH_AUDIENCE: str = "" # e.g., "https://yourapi.com"
    TENANCY_ENABLED: bool = True
    API_KEY: str = "secret"

    # Authentication
    ENABLE_API_KEY_AUTH: bool = False  # Set to True in production
    ENABLE_JWT_AUTH: bool = False  # Set to True when using JWT tokens
    SECRET_KEY: str = "change-this-secret-key-in-production"  # For JWT signing

    # Rate Limiting
    ENABLE_RATE_LIMITING: bool = False  # Set to True in production
    RATE_LIMIT_REQUESTS: int = 100  # Max requests per window
    RATE_LIMIT_WINDOW: int = 60  # Time window in seconds

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8501"]
    
    # --- LLM Provider API Keys ---
    # These are loaded from environment variables automatically by pydantic-settings.
    # Add any new provider keys here for awareness, even if not defined as a field.
    #
    # MISTRAL_API_KEY: str | None = None
    # DEEPSEEK_API_KEY: str | None = None
    # DASHSCOPE_API_KEY: str | None = None (for Qwen)
    
    # Celery settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Memory lifecycle settings
    MEMORY_RETENTION_DAYS: int = 30
    MEMORY_DECAY_RATE: float = 0.99

    # Logging configuration
    LOG_LEVEL: str = "WARNING"  # For external libraries (uvicorn, asyncpg, etc.)
    RAE_APP_LOG_LEVEL: str = "INFO"  # For RAE application logs

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
