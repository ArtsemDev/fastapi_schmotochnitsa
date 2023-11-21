from datetime import datetime

from sqladmin.fields import DateTimeField, SelectField
from sqlalchemy import select
from wtforms import Form, TextAreaField, StringField, DecimalField, BooleanField
from wtforms.validators import length, number_range
from slugify import slugify

from core.database import Category, session


__all__ = [
    "AdvertForm",
    "CategoryForm"
]


class CategoryForm(Form):
    name = StringField(
        label="Название"
    )
    slug = StringField(
        label="URL",
        default=None
    )

    def validate_slug(self, field):
        self.slug.data = slugify(self.name.data)


def load_categories():
    with session() as s:
        obj = s.scalars(
            select(Category)
            .order_by(Category.id)
        )
        return [(cat.id, cat.name) for cat in obj.all()]


class AdvertForm(Form):
    title = StringField(
        label="Заголовок",
        validators=[
            length(min=2, max=128, message="Заголовок должен быть от 2 до 128 символов")
        ]
    )
    body = TextAreaField(
        label="Описание",
        validators=[
            length(min=50, max=250)
        ]
    )
    price = DecimalField(
        label="Цена",
        validators=[
            number_range(
                min=1,
                max=99999999.99
            )
        ]
    )
    date_created = DateTimeField(
        label="Дата создания",
        default=datetime.utcnow
    )
    category_id = SelectField(
        label="Категория",
        choices=load_categories
    )
    is_published = BooleanField(
        label="Опубликовано",
        default=False
    )
    slug = StringField(
        label="URL",
        default=None
    )

    def validate_slug(self, field):
        self.slug.data = slugify(f"{self.title.data}{self.date_created.data.timestamp()}")
