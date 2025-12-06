"""
Application Configuration

This module uses Pydantic Settings to manage configuration from environment
variables and .env files. This is a best practice for 12-factor apps.

Educational Note:
- Environment variables allow different configs for dev/staging/production
- Pydantic provides type validation and helpful error messages
- Never hardcode secrets or environment-specific values
"""

from typing import List

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "The Wizard's Keep"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # API
    API_HOST: str = "0.0.0.0"  # nosec B104 - Bind all interfaces for development
    API_PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    # CORS - Define which origins can access the API
    CORS_ORIGINS: List[str] = [
        "http://localhost:8080",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
    ]

    # Database
    DATABASE_URL: PostgresDsn = (
        "postgresql://wizard:wizard123@localhost:5432/wizards_keep"  # type: ignore
    )
    POSTGRES_USER: str = "wizard"
    POSTGRES_PASSWORD: str = "wizard123"
    POSTGRES_DB: str = "wizards_keep"

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Game Configuration
    MAX_PLAYER_NAME_LENGTH: int = 50
    STARTING_HEALTH: int = 100
    STARTING_LOCATION_ID: int = 1

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


# Create global settings instance
settings = Settings()
