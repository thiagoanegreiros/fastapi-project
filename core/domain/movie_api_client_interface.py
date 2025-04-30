from typing import List, Optional, Protocol

from core.domain.movie import Movie


class IMovieGateway(Protocol):
    def find_all(self, query: str) -> List[Movie]: ...

    def popular(self) -> List[Movie]: ...

    def get(self, id: int) -> Optional[Movie]: ...
