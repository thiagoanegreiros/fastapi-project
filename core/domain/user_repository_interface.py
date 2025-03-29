from typing import List, Optional, Protocol

from core.domain.user import User


class IUserRepository(Protocol):
    """Interface para repositórios de usuário"""

    def save(self, user: User) -> User: ...

    def find_all(self) -> List[User]: ...

    def delete(self, id: str) -> bool: ...

    def get(self, id: str) -> Optional[User]: ...
