"""This module contain CleanPathMiddleware"""

from starlette.datastructures import URL
from starlette.types import ASGIApp, Scope, Receive, Send
from fastapi import status
from fastapi.responses import RedirectResponse


__all__ = ["CleanPathMiddleware"]


class CleanPathMiddleware:
    """Middleware that corrects duplicates of '//' in a user request"""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if "//" in scope.get("path"):

            while "//" in scope.get("path"):
                scope["path"] = scope.get("path").replace("//", "/")

            url = URL(scope=scope)
            response = RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
            await response(scope=scope, receive=receive, send=send)
            return

        await self.app(scope, receive, send)
