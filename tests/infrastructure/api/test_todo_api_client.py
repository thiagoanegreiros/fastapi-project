from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import HTTPStatusError, Request, Response

from core.domain.todo import ToDo
from infrastructure.api.todo_api_client import TodoApiClient


@pytest.fixture
def client():
    return TodoApiClient(base_url="https://fakeapi.com")


@pytest.mark.asyncio
async def test_find_all(client):
    todos_data = [
        {"id": 1, "userId": 1, "title": "Estudar", "completed": False},
        {"id": 2, "userId": 2, "title": "Comprar pão", "completed": True},
    ]

    mock_response = MagicMock()
    mock_response.json.return_value = todos_data  # <-- método síncrono
    mock_response.raise_for_status.return_value = None  # <-- método síncrono

    with patch(
        "httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)
    ) as mock_get:
        result = await client.find_all()

        mock_get.assert_called_once_with("https://fakeapi.com/todos")
        assert result == [ToDo.model_validate(todo) for todo in todos_data]


@pytest.mark.asyncio
async def test_get(client):
    todo_data = {"id": 1, "userId": 1, "title": "Estudar", "completed": False}

    mock_response = MagicMock()
    mock_response.json.return_value = todo_data
    mock_response.raise_for_status.return_value = None

    with patch(
        "httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)
    ) as mock_get:
        result = await client.get(1)

        mock_get.assert_called_once_with("https://fakeapi.com/todos/1")
        assert result == ToDo.model_validate(todo_data)


@pytest.mark.asyncio
async def test_find_all_http_error(client):
    with patch("httpx.AsyncClient.get", new=AsyncMock()) as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPStatusError(
            "Erro",
            request=Request("GET", "https://fakeapi.com/todos"),
            response=Response(500),
        )
        mock_get.return_value = mock_response

        with pytest.raises(HTTPStatusError):
            await client.find_all()


@pytest.mark.asyncio
async def test_get_http_error(client):
    with patch("httpx.AsyncClient.get", new=AsyncMock()) as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPStatusError(
            "Erro",
            request=Request("GET", "https://fakeapi.com/todos/1"),
            response=Response(404),
        )
        mock_get.return_value = mock_response

        with pytest.raises(HTTPStatusError):
            await client.get(1)
