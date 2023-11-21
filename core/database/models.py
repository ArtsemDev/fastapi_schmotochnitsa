from sqlalchemy import (
    Column,
    SMALLINT,
    VARCHAR,
    CheckConstraint,
    INT,
    DECIMAL,
    ForeignKey,
    TIMESTAMP,
    BOOLEAN
)
from sqlalchemy.orm import relationship

from .base import Base


__all__ = [
    "Base",
    "Advert",
    "Category",
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
