from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from sqladmin import Admin
from redis.asyncio import Redis

from core.database import engine
from core.admin import CategoryAdmin, AdvertAdmin
from core.middleware import JWTAuthenticationBackend, SessionAuthenticationBackend
from core.exception_handlers import not_authenticated

from api import router as api_router
from core.settings import settings, static
from web.views import router as web_router

app = FastAPI(
    title="Шмоточница",
    summary="Доска объявлений",
    default_response_class=ORJSONResponse,
    exception_handlers={
        401: not_authenticated
    }
)
app.mount(
    path="/static",
    app=static,
    name="static"
)
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


@app.on_event("startup")
async def startup():
    redis = Redis.from_url(url=settings.REDIS_URL.unicode_string())
    FastAPICache.init(backend=RedisBackend(redis), prefix="fastapi-cache")
