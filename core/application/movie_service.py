from typing import List, Optional

from core.domain.movie import Movie
from core.domain.movie_api_client_interface import IMovieGateway
from core.logger.logger import Logger


class MovieService:
    def __init__(
        self,
        gateway: IMovieGateway,
        logger: Logger,
    ):
        self.gateway = gateway
        self.logger = logger

    def find_all(self, query: str) -> List[Movie]:
        return self.gateway.find_all(query)

    def popular(self) -> List[Movie]:
        return self.gateway.popular()

    def get(self, id: str) -> Optional[Movie]:
        return self.gateway.get(id)
