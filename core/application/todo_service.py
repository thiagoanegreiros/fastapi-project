from typing import List, Optional

from core.domain.todo import ToDo
from core.domain.todo_api_client_interface import ITodoGateway
from core.logger.logger import Logger


class TodoService:
    """Serviço de Usuário desacoplado de repositórios específicos"""

    def __init__(
        self,
        gateway: ITodoGateway,
        logger: Logger,
    ):
        self.gateway = gateway
        self.logger = logger

    def find_all(self) -> List[ToDo]:
        self.logger.info("Buscando todos os ToDos")
        return self.gateway.find_all()

    def get(self, id: str) -> Optional[ToDo]:
        self.logger.debug(f"Buscando ToDo com ID: {id}")
        return self.gateway.get(id)
