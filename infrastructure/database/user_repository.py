from typing import List
from sqlmodel import Session
from core.domain.user import User
from core.domain.user_repository_interface import IUserRepository
from infrastructure.database.models import UserDB
from infrastructure.database.base_repository import BaseRepository

class UserRepository(BaseRepository[UserDB], IUserRepository):
    def __init__(self, session: Session):
        super().__init__(session, UserDB)

    def get(self, id: str) -> User | None:
        user_db = super().get(id)
        return User.model_validate(user_db) if user_db else None

    def find_all(self) -> List[User]:
        users_db = super().find_all()
        return [User.model_validate(u) for u in users_db]

    def save(self, user: User) -> User:
        user_db = UserDB(**user.model_dump())
        saved = super().save(user_db)
        return User.model_validate(saved)

    def delete(self, id: str) -> bool:
        return super().delete(id)
