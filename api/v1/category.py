from fastapi import APIRouter, Path
# from fastapi_cache.decorator import cache

from core.dependencies import IsAuthenticated
from core.repositories.category import Category
from core.types import CategoryDetail

router = APIRouter()


@router.get(
    path="/categories",
    response_model=list[CategoryDetail],
    name="category_list"
)
async def category_list(manager: Category):
    return manager.all()


@router.get(
    path="/categories/{pk}",
    response_model=CategoryDetail,
    dependencies=[IsAuthenticated],
    name="category_detail"
)
async def category_detail(manager: Category, pk: int = Path(ge=1, examples=[42])):
    return manager.get(pk=pk)
