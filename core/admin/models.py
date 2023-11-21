from sqladmin import ModelView

from ..database import Advert, Category
from ..forms import AdvertForm, CategoryForm


__all__ = [
    "AdvertAdmin",
    "CategoryAdmin"
]


class AdvertAdmin(ModelView, model=Advert):
    name_plural = "объявление"
    column_list = ["title", "is_published", "date_created"]
    form = AdvertForm


class CategoryAdmin(ModelView, model=Category):
    name_plural = "категория"
    column_list = ["name"]
    form = CategoryForm
