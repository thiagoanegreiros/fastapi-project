from typing import List

import httpx

from core.domain.todo import ToDo
from core.domain.todo_api_client_interface import ITodoGateway


class TodoApiClient(ITodoGateway):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def find_all(self) -> List[ToDo]:
        response = httpx.get(f"{self.base_url}/todos")
        response.raise_for_status()
        todos_data = response.json()
        return [ToDo.model_validate(todo) for todo in todos_data]

    def get(self, id: int) -> ToDo:
        response = httpx.get(f"{self.base_url}/todos/{id}")
        response.raise_for_status()
        todo_data = response.json()
        return ToDo.model_validate(todo_data)
