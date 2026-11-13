"""Application settings, loaded from environment variables and `backend/.env`."""

from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Application -----------------------------------------------------
    app_name: str = "TerangaFlow API"
    app_version: str = "0.1.0"
    app_env: Literal["development", "staging", "production", "test"] = "development"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    # Comma-separated list in the environment, e.g. "http://localhost:5173,http://127.0.0.1:5173"
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )

    # --- Database (Supabase PostgreSQL) -----------------------------------
    # Kept as a secret so it is never printed in logs or reprs.
    database_url: SecretStr | None = None
    db_pool_size: int = Field(default=5, ge=1)
    db_max_overflow: int = Field(default=5, ge=0)
    db_pool_timeout: int = Field(default=30, ge=1)
    db_pool_recycle: int = Field(default=1800, ge=-1)
    db_connect_timeout: int = Field(default=10, ge=1)
    db_echo: bool = False

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("database_url", mode="before")
    @classmethod
    def _empty_url_is_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @property
    def is_database_configured(self) -> bool:
        return self.database_url is not None

    @property
    def sqlalchemy_database_url(self) -> str:
        """Database URL normalised for SQLAlchemy + psycopg 3.

        Supabase gives URLs starting with `postgresql://` or `postgres://`;
        both are rewritten to the explicit `postgresql+psycopg://` driver.
        """
        if self.database_url is None:
            raise RuntimeError("DATABASE_URL is not configured.")
        url = self.database_url.get_secret_value().strip()
        for prefix in ("postgresql+psycopg://", "postgresql://", "postgres://"):
            if url.startswith(prefix):
                return "postgresql+psycopg://" + url[len(prefix) :]
        raise ValueError("DATABASE_URL must be a PostgreSQL URL (postgresql://...).")


@lru_cache
def get_settings() -> Settings:
    return Settings()
