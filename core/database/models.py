from sqlalchemy import (
    Column,
    SMALLINT,
    VARCHAR,
    CheckConstraint,
    INT,
    DECIMAL,
    ForeignKey,
    TIMESTAMP,
    BOOLEAN, CHAR
)
from sqlalchemy.orm import relationship
from ulid import parse

from .base import Base


__all__ = [
    "Base",
    "Advert",
    "Category",
    "User",
]


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint("length(name) >= 2"),
        CheckConstraint("length(slug) >= 2"),
        CheckConstraint("slug not like '% %'"),
    )

    id = Column(SMALLINT, primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)
    slug = Column(VARCHAR(32), nullable=False, unique=True)

    adverts = relationship(argument="Advert", back_populates="category")

    def __str__(self):
        return self.name


class Advert(Base):
    __tablename__ = "adverts"
    __table_args__ = (
        CheckConstraint("length(title) >= 2"),
        CheckConstraint("length(body) >= 50"),
        CheckConstraint("price > 0"),
    )

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(128), nullable=False)
    body = Column(VARCHAR(250), nullable=False)
    price = Column(DECIMAL(precision=10, scale=2), nullable=False)
    category_id = Column(
        SMALLINT,
        ForeignKey("categories.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )
    date_created = Column(TIMESTAMP, nullable=False)
    is_published = Column(BOOLEAN, default=False)
    slug = Column(VARCHAR(128), nullable=True, unique=True)

    category = relationship(argument="Category", back_populates="adverts")

    def __str__(self):
        return self.title


class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(26), primary_key=True)
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(CHAR(60), nullable=False)
    is_active = Column(BOOLEAN, default=False)
    is_staff = Column(BOOLEAN, default=False)

    @property
    def date_register(self):
        return parse(self.id).timestamp().datetime

    def __str__(self) -> str:
        return self.email
