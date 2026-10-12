from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ForwardCheck AI API"
    environment: str = "development"
    database_url: str = "sqlite:///./forwardcheck.db"
    frontend_origin: str = "http://localhost:3000"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    brave_search_api_key: str | None = None
    max_source_bytes: int = Field(default=2_000_000, ge=100_000, le=10_000_000)
    source_timeout_seconds: float = Field(default=10.0, ge=1, le=30)
    max_claims: int = Field(default=12, ge=1, le=30)
    max_sources_per_claim: int = Field(default=4, ge=1, le=10)


@lru_cache
def get_settings() -> Settings:
    return Settings()
