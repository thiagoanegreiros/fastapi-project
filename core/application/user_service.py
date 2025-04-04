from typing import List, Optional

from core.domain.user import User
from core.domain.user_repository_interface import IUserRepository


class UserService:
    """Serviço de Usuário desacoplado de repositórios específicos"""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def save(self, user: User) -> User:
        return self.user_repository.save(user)

    def find_all(self) -> List[User]:
        return self.user_repository.find_all()

    def delete(self, id: str) -> bool:
        return self.user_repository.delete(id)

    def get(self, id: str) -> Optional[User]:
        return self.user_repository.get(id)
