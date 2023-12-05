from http.client import HTTPException

from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def not_authenticated(request: Request, exc: HTTPException):
    return RedirectResponse(url=request.app.url_path_for("login"))


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": [{"msg": err.get("msg"), "input": err.get("input")} for err in exc.errors()]},
    )
