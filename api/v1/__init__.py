from fastapi import APIRouter

from .category import category_router


__all__ = ["router"]


router = APIRouter(
    prefix="/v1"
)
router.include_router(router=category_router.router)
