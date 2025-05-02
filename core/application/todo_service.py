from typing import List, Optional

from core.domain.todo import ToDo
from core.domain.todo_api_client_interface import ITodoGateway
from core.logger.logger import Logger


class TodoService:
    def __init__(
        self,
        gateway: ITodoGateway,
        logger: Logger,
    ):
        self.gateway = gateway
        self.logger = logger

    async def find_all(self) -> List[ToDo]:
        return await self.gateway.find_all()

    async def get(self, id: str) -> Optional[ToDo]:
        return await self.gateway.get(id)
