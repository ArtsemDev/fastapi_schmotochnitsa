from decimal import Decimal
from typing import Optional
from datetime import datetime

from pydantic import Field, PositiveInt

from .base import Schema


__all__ = [
    "AdvertCreate",
    "AdvertEdit",
    "AdvertDetail"
]


class AdvertCreate(Schema):
    title: str = Field(
        default=...,
        title="Advert Title",
        min_length=2,
        max_length=128,
        examples=["I will sell the garage"]
    )
    body: str = Field(
        default=...,
        min_length=50,
        max_length=250,
        title="Advert Description",
        examples=["Very good ...!"]
    )
    price: Decimal = Field(
        default=...,
        max_digits=10,
        decimal_places=2,
        title="Garage Price",
        examples=[41.99],
        gt=0
    )
    category_id: PositiveInt = Field(
        default=...,
        title="Advert Category ID",
        examples=[42]
    )
    date_created: datetime = Field(
        default_factory=datetime.utcnow
    )
    is_published: bool = Field(default=False)


class AdvertEdit(AdvertCreate):
    ...


class AdvertDetail(AdvertCreate):
    id: PositiveInt = Field(
        default=...,
        title="Advert ID",
        examples=[42]
    )
