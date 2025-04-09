from typing import List, Optional

from core.domain.user import User
from core.domain.user_repository_interface import IUserRepository
from core.logger.logger import Logger  # ok importar isso


class UserService:
    """Serviço de Usuário desacoplado de repositórios específicos"""

    def __init__(
        self,
        user_repository: IUserRepository,
        logger: Logger,
    ):
        self.user_repository = user_repository
        self.logger = logger

    def save(self, user: User) -> User:
        self.logger.info(f"Salvando usuário: {user}")
        return self.user_repository.save(user)

    def find_all(self) -> List[User]:
        self.logger.info("Buscando todos os usuários")
        return self.user_repository.find_all()

    def delete(self, id: str) -> bool:
        self.logger.warning(f"Deletando usuário com ID: {id}")
        return self.user_repository.delete(id)

    def get(self, id: str) -> Optional[User]:
        self.logger.debug(f"Buscando usuário com ID: {id}")
        return self.user_repository.get(id)
