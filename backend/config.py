"""Configuration module for the RentBack backend."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the backend directory (where this file lives)
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)


class Settings:
    """Application settings loaded from environment variables."""

    # LLM Provider
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # Mistral
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL: str = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
    
    # Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    
    # Data Source
    DATA_SOURCE: str = os.getenv("DATA_SOURCE", "mock")
    RENTCAST_API_KEY: str = os.getenv("RENTCAST_API_KEY", "")
    
    # App Settings
    DEFAULT_CITY: str = os.getenv("DEFAULT_CITY", "nyc")
    SEARCH_RADIUS_MILES: float = float(os.getenv("SEARCH_RADIUS_MILES", "0.5"))
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")


settings = Settings()
