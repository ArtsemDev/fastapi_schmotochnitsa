from fastapi import APIRouter, Path

from core.repositories.category import category_manager, Category

router = APIRouter()


class Router:

    def __init__(self, manager):
        self.manager = manager
        self.router = APIRouter(
            tags=[self.manager.repository.model.__tablename__.title()]
        )
        prefix = f"/{self.manager.repository.model.__tablename__}"
        self.router.get(
            path=prefix,
            response_model=self.manager.repository.schema
        )(self.all)
        self.router.get(
            path=prefix + "/{pk}",
            response_model=list[self.manager.repository.schema]
        )(self.get)
        self.router.delete(
            path=prefix + "/{pk}"
        )(self.delete)

    async def all(self):
        return self.manager.all()

    async def get(self, pk: int = Path(ge=1, example=42)):
        return self.manager.get(pk=pk)

    async def update(self, pk: int = Path(ge=1, example=42)):
        pass

    async def delete(self, pk: int = Path(ge=1, example=42)):
        return self.manager.delete(pk=pk)


category_router = Router(
    manager=category_manager,
)
