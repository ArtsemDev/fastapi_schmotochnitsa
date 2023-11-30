# from datetime import datetime
from pathlib import Path

from passlib.context import CryptContext
from pydantic import PostgresDsn, SecretStr, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

__all__ = ["settings", "pwd_context", "static", "templating"]


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
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    EXP_JWT: int
    YANDEX_APP_PASSWORD: SecretStr
    YANDEX_HOST: str
    YANDEX_PORT: int
    YANDEX_USER: str


settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis = Redis.from_url(url=settings.REDIS_URL.unicode_string())
static = StaticFiles(
    directory=settings.BASE_DIR / "static"
)
templating = Jinja2Templates(
    directory=settings.BASE_DIR / "templates"
)
# templating.env.globals["time_now"] = datetime.utcnow
