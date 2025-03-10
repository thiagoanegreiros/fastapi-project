from core.domain.user_repository_interface import IUserRepository
from core.domain.user import User
from typing import List
import uuid

class UserRepository(IUserRepository):
    """Implementação concreta do UserRepository"""

    def __init__(self):
        self.users = []

    def save(self, user: User) -> User:
        """Gera ID automaticamente e salva o usuário"""
        user.id = str(uuid.uuid4())
        self.users.append(user)
        return user

    def get_all(self) -> List[User]:
        return self.users
