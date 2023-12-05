import contextlib
import logging

from fastapi import FastAPI
from fastapi.applications import AppType
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from sqladmin import Admin
from redis.asyncio import Redis

from core.database import engine
from core.admin import CategoryAdmin, AdvertAdmin
from core.middleware import SessionAuthenticationBackend, CleanPathMiddleware
from core.exception_handlers import not_authenticated, request_validation_exception_handler

from api import router as api_router
from core.settings import settings, static
from core.types import HTTPValidationError
from web.views import router as web_router


@contextlib.asynccontextmanager
async def lifespan(app: AppType):
    # redis = Redis.from_url(url=settings.REDIS_URL.unicode_string())
    # FastAPICache.init(backend=RedisBackend(redis), prefix="fastapi-cache")
    yield
    logging.info("SHUTDOWN")


app = FastAPI(
    title="Шмоточница",
    summary="Доска объявлений",
    default_response_class=ORJSONResponse,
    exception_handlers={
        401: not_authenticated,
        RequestValidationError: request_validation_exception_handler
    },
    responses={
        422: {
            "model": HTTPValidationError
        }
    },
    lifespan=lifespan
)
app.mount(
    path="/static",
    app=static,
    name="static"
)
app.add_middleware(CleanPathMiddleware)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=("0.0.0.0", "127.0.0.1", "*"),
    allow_methods=("GET", "POST", "PATCH", "DELETE", "HEAD")
)
# app.add_middleware(
#     middleware_class=AuthenticationMiddleware,
#     backend=JWTAuthenticationBackend()
# )
app.add_middleware(
    middleware_class=AuthenticationMiddleware,
    backend=SessionAuthenticationBackend()
)
app.include_router(router=web_router)
app.include_router(router=api_router)
admin = Admin(app=app, engine=engine)
admin.add_view(view=AdvertAdmin)
admin.add_view(view=CategoryAdmin)


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="0.0.0.0",
        port=8000,
        use_colors=True
    )
