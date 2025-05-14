from typing import Any, List, Optional

from domain.user import User
from domain.user_repository_interface import IUserRepository
from infrastructure.logger.logger import Logger  # ok importar isso


class UserService:
    """Serviço de Usuário desacoplado de repositórios específicos"""

    def __init__(
        self,
        user_repository: IUserRepository,
        logger: Logger,
    ):
        self.user_repository = user_repository
        self.logger = logger

    async def save(self, user: User) -> User:
        self.logger.info(f"Salvando usuário: {user}")
        return await self.user_repository.save(user)

    async def find_all(self) -> List[User]:
        self.logger.info("Buscando todos os usuários")
        return await self.user_repository.find_all()

    async def delete(self, id: str) -> bool:
        self.logger.warning(f"Deletando usuário com ID: {id}")
        return await self.user_repository.delete(id)

    async def get(self, id: str) -> Optional[User]:
        self.logger.debug(f"Buscando usuário com ID: {id}")
        return await self.user_repository.get(id)

    async def update(self, user_id: str, user_data: dict[str, Any]) -> User | None:
        return await self.user_repository.update(user_id, user_data)
