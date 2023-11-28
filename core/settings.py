from pathlib import Path

from passlib.context import CryptContext
from pydantic import PostgresDsn, SecretStr, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis

__all__ = ["settings", "pwd_context"]


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
    EXP_JWT: int
    YANDEX_APP_PASSWORD: SecretStr
    YANDEX_HOST: str
    YANDEX_PORT: int
    YANDEX_USER: str


settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis = Redis.from_url(url=settings.REDIS_URL.unicode_string())
