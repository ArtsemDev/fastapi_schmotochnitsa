from http.client import HTTPException

from starlette.requests import Request
from starlette.responses import RedirectResponse


async def not_authenticated(request: Request, exc: HTTPException):
    return RedirectResponse(url="/login")
