"""
MarketPulse AI — Application Configuration
All settings loaded from environment variables with secure defaults.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings. Never hard-code secrets."""

    # --- Application ---
    APP_NAME: str = "MarketPulse AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    DEMO_MODE: bool = True
    LOG_LEVEL: str = "INFO"

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://marketpulse:marketpulse_dev_password@localhost:5432/marketpulse"
    DATABASE_SYNC_URL: str = "postgresql+psycopg2://marketpulse:marketpulse_dev_password@localhost:5432/marketpulse"

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- Security ---
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: str = "http://localhost:3000"
    RATE_LIMIT_PER_MINUTE: int = 60

    # --- Market Data Providers ---
    ALPHA_VANTAGE_API_KEY: str = ""
    COINGECKO_API_KEY: str = ""

    # --- Email ---
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
