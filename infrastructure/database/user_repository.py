import uuid
from typing import List, Optional

from core.domain.user import User
from core.domain.user_repository_interface import IUserRepository


class UserRepository(IUserRepository):
    """Implementação concreta do UserRepository"""

    def __init__(self):
        self.users = []

    def save(self, user: User) -> User:
        """Gera ID automaticamente e salva o usuário"""
        user.id = str(uuid.uuid4())
        self.users.append(user)
        return user

    def find_all(self) -> List[User]:
        return self.users

    def delete(self, id: str) -> None:
        for u in self.users:
            if u.id == id:
                self.users.remove(u)
                break

    def get(self, id: str) -> Optional[User]:
        for u in self.users:
            if u.id == id:
                return u
        return None
