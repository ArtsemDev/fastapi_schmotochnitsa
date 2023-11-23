from fastapi import APIRouter, Path
from fastapi_cache.decorator import cache

from core.repositories.category import category_manager, Category
from core.types import CategoryDetail
from core.tasks import ping

router = APIRouter()


@router.get(
    path="/categories",
    response_model=list[CategoryDetail]
)
@cache(expire=60)
async def all_categories(manager: Category):
    ping.delay()
    return manager.all()


@router.get(
    path="/categories/{pk}",
    response_model=CategoryDetail
)
@cache(expire=60)
async def get(manager: Category, pk: int = Path(ge=1, example=42)):
    return manager.get(pk=pk)


async def update(self, pk: int = Path(ge=1, example=42)):
    pass


async def delete(self, pk: int = Path(ge=1, example=42)):
    return self.manager.delete(pk=pk)
