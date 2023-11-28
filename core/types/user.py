from datetime import datetime
from typing import Self, Optional

from pydantic import EmailStr, model_validator, Field
from ulid import new

from .base import Schema
from .custom import PasswordStr
from core.settings import pwd_context


__all__ = [
    "UserRegisterForm",
    "UserLoginForm",
    "UserDetail"
]


class UserLoginForm(Schema):
    email: EmailStr
    password: PasswordStr

    def validate_password(self, hash_password: str) -> bool:
        return pwd_context.verify(self.password, hash_password)


class UserRegisterForm(UserLoginForm):
    confirm_password: PasswordStr

    @model_validator(mode="after")
    def password_match_validator(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("password and confirm password does not match")

        return self


class UserDetail(Schema):
    id: str = Field(
        default_factory=lambda: new().str,
        min_length=26,
        max_length=26
    )
    email: EmailStr
    date_register: Optional[datetime] = Field(default=None)
    password: str
    is_active: bool = Field(default=False)
    is_staff: bool = Field(default=False)

    @classmethod
    def create(cls, data: UserRegisterForm) -> Self:
        return cls(
            email=data.email,
            password=pwd_context.hash(data.password)
        )
