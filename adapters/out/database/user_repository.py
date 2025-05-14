from typing import Any, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from adapters.out.database.base_repository import BaseRepository
from adapters.out.database.models import UserDB
from domain.user import User
from domain.user_repository_interface import IUserRepository


class UserRepository(BaseRepository[UserDB], IUserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserDB)

    async def get(self, id: str) -> User | None:
        user_db = await super().get(id)
        return User.model_validate(user_db) if user_db else None

    async def find_all(self) -> List[User]:
        users_db = await super().find_all()
        return [User.model_validate(u) for u in users_db]

    async def save(self, user: User) -> User:
        user_db = UserDB(**user.model_dump())
        saved = await super().save(user_db)
        return User.model_validate(saved)

    async def delete(self, id: str) -> bool:
        return await super().delete(id)

    async def update(self, id: str, data: dict[str, Any]) -> Optional[User]:
        return await super().update(id, data)
