from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from core.database import engine
from core.admin import CategoryAdmin, AdvertAdmin

from api import router as api_router


app = FastAPI(
    title="Шмоточница",
    summary="Доска объявлений",
    default_response_class=ORJSONResponse,
)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=("0.0.0.0", "127.0.0.1", "*"),
    allow_methods=("GET", "POST", "PATCH", "DELETE", "HEAD")
)
app.include_router(router=api_router)
admin = Admin(app=app, engine=engine)
admin.add_view(view=AdvertAdmin)
admin.add_view(view=CategoryAdmin)
