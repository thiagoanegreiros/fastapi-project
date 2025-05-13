from typing import Generic, List, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get(self, id: str) -> T | None:
        return await self.session.get(self.model, id)

    async def find_all(self) -> List[T]:
        statement = select(self.model)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def save(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete(self, id: str) -> bool:
        obj = await self.get(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False
