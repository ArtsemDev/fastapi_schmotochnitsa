from typing import Any

from pydantic import BaseModel


__all__ = ["ValidationError", "HTTPValidationError"]


class ValidationError(BaseModel):
    msg: str
    input: Any


class HTTPValidationError(BaseModel):
    detail: list[ValidationError]
