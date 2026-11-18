"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Validated worker settings.

    Environment variable names are case-insensitive and loaded from ``.env``
    when it exists. Secrets use ``SecretStr`` so accidental logging does not
    reveal their values.
    """

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "TAI TTS Worker"
    app_version: str = "1.0.0"
    worker_api_key: SecretStr = Field(min_length=1)
    gemini_api_key: SecretStr | None = None
    gemini_model: str = "gemini-2.5-flash"
    gemini_timeout_ms: int = Field(default=30_000, ge=1_000)

    tts_voice: str = "vi-VN-HoaiMyNeural"
    tts_rate: str = "+0%"
    tts_max_retries: int = Field(default=4, ge=1, le=10)

    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65_535)


@lru_cache
def get_settings() -> Settings:
    """Return one immutable-by-convention settings instance per process."""

    return Settings()
