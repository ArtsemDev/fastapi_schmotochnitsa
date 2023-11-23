from pathlib import Path

from pydantic import PostgresDsn, SecretStr, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        frozen=True
    )

    DATABASE_URL: PostgresDsn
    SECRET_KEY: SecretStr
    REDIS_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn
    CELERY_BROKER_URL: RedisDsn
    BASE_DIR: Path = Path(__file__).resolve().parent


settings = Settings()
