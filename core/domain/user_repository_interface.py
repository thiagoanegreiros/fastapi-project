from typing import List, Protocol

from core.domain.user import User


class IUserRepository(Protocol):
    """Interface para repositórios de usuário"""

    def save(self, user: User) -> User:
        """Salva um usuário no banco"""
        ...

    def find_all(self) -> List[User]:
        """Retorna todos os usuários"""
        ...
