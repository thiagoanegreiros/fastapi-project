from typing import List

import httpx

from domain.todo import ToDo
from domain.todo_api_client_interface import ITodoGateway


class TodoApiClient(ITodoGateway):
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def find_all(self) -> List[ToDo]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/todos")
            response.raise_for_status()
            todos_data = response.json()
            return [ToDo.model_validate(todo) for todo in todos_data]

    async def get(self, id: int) -> ToDo:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/todos/{id}")
            response.raise_for_status()
            todo_data = response.json()
            return ToDo.model_validate(todo_data)
