from typing import List
from typing import Optional

from core.domain.user import User
from core.domain.user_repository_interface import IUserRepository


class UserService:
    """Serviço de Usuário desacoplado de repositórios específicos"""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        return self.user_repository.save(user)

    def list_users(self) -> List[User]:
        return self.user_repository.find_all()

    def delete_user(self, id: str) -> None:
        return self.user_repository.delete(id)

    def get_user(self, id: str) -> Optional[User]:
        return self.user_repository.get(id)
