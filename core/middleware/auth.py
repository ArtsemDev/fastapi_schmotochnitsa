import typing

from starlette.middleware.authentication import AuthenticationBackend, AuthCredentials, AuthenticationError
from starlette.requests import HTTPConnection

from core.repositories import user_repository
from core.utils import verify_jwt_token


__all__ = ["JWTAuthenticationBackend"]


class AuthenticatedUser:

    def __init__(self, identity: str, email: str) -> None:
        self.is_authenticated = True
        self.identity = identity
        self.display_name = email


class JWTAuthenticationBackend(AuthenticationBackend):

    async def authenticate(
        self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple["AuthCredentials", "AuthenticatedUser"]]:
        if "Authorization" not in conn.headers:
            return

        token = conn.headers.get("Authorization")
        try:
            user_id = verify_jwt_token(jwt_token=token)
        except ValueError as e:
            return
        else:
            user = user_repository.get(pk=user_id)
            if user is None:
                return
            return AuthCredentials(["authenticated"]), AuthenticatedUser(identity=user_id, email=user.email)
