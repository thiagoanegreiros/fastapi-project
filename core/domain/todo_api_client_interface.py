from typing import List, Optional, Protocol

from core.domain.todo import ToDo


class ITodoGateway(Protocol):
    def find_all(self) -> List[ToDo]: ...

    def get(self, id: int) -> Optional[ToDo]: ...
