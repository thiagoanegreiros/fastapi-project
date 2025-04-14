from unittest.mock import Mock, patch

import pytest
from httpx import HTTPStatusError, Request, Response

from core.domain.todo import ToDo
from infrastructure.api.todo_api_client import TodoApiClient


@pytest.fixture
def client():
    return TodoApiClient(base_url="https://fakeapi.com")


def test_find_all(client):
    # Arrange
    todos_data = [
        {"id": 1, "userId": 1, "title": "Estudar", "completed": False},
        {"id": 2, "userId": 2, "title": "Comprar pão", "completed": True},
    ]
    mock_response = Mock()
    mock_response.json.return_value = todos_data
    mock_response.raise_for_status.return_value = None

    with patch("httpx.get", return_value=mock_response) as mock_get:
        # Act
        result = client.find_all()

        # Assert
        mock_get.assert_called_once_with("https://fakeapi.com/todos")
        assert result == [ToDo.model_validate(todo) for todo in todos_data]


def test_get(client):
    # Arrange
    todo_data = {"id": 1, "userId": 1, "title": "Estudar", "completed": False}
    mock_response = Mock()
    mock_response.json.return_value = todo_data
    mock_response.raise_for_status.return_value = None

    with patch("httpx.get", return_value=mock_response) as mock_get:
        # Act
        result = client.get(1)

        # Assert
        mock_get.assert_called_once_with("https://fakeapi.com/todos/1")
        assert result == ToDo.model_validate(todo_data)


def test_find_all_http_error(client):
    # Arrange
    with patch("httpx.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = HTTPStatusError(
            "Error",
            request=Request("GET", "https://fakeapi.com/todos"),
            response=Response(500),
        )

        # Act & Assert
        with pytest.raises(HTTPStatusError):
            client.find_all()


def test_get_http_error(client):
    # Arrange
    with patch("httpx.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = HTTPStatusError(
            "Error",
            request=Request("GET", "https://fakeapi.com/todos/1"),
            response=Response(404),
        )

        # Act & Assert
        with pytest.raises(HTTPStatusError):
            client.get(1)
