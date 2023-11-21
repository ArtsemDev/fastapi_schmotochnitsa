from pydantic import PositiveInt, Field

from .base import Schema
from .custom import SlugStr


__all__ = [
    "CategoryDetail"
]


class CategoryDetail(Schema):
    id: PositiveInt = Field(
        default=...,
        title="Category ID",
        examples=[42]
    )
    name: str = Field(
        default=...,
        title="Category Name",
        min_length=2,
        max_length=32,
        examples=["Auto"]
    )
    slug: SlugStr = Field(
        default=...,
        title="Category URL",
        min_length=2,
        max_length=32,
        examples=["mobile-phones"]
    )
