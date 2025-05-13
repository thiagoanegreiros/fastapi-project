from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from adapters.inbound.routes import todo_router
from domain.todo import ToDo
from infrastructure.container import Container
from infrastructure.logger.logger import Logger
from infrastructure.logger.logger_middleware import RequestLoggingMiddleware


@pytest.fixture
def client_and_gateway():
    container = Container()

    # ✅ Mocks assíncronos
    mock_gateway = MagicMock()
    mock_gateway.find_all = AsyncMock()
    mock_gateway.get = AsyncMock()

    mock_logger = MagicMock(spec=Logger)

    container.todo_service.override(mock_gateway)
    container.logger.override(mock_logger)
    container.wire(
        modules=[
            "adapters.inbound.routes.todo_router",
            "infrastructure.logger.logger_middleware",
        ]
    )

    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    app.container = container
    app.include_router(todo_router.router)

    client = TestClient(app, raise_server_exceptions=True)

    return client, mock_gateway


def test_list_todos(client_and_gateway):
    client, mock_gateway = client_and_gateway
    todo1 = ToDo(id=1, userId=1, title="Start Learning", completed=True)
    todo2 = ToDo(id=2, userId=1, title="Finish Azure AZ-104", completed=False)

    mock_gateway.find_all.return_value = [todo1, todo2]

    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == [todo1.model_dump(), todo2.model_dump()]
    mock_gateway.find_all.assert_awaited_once()


def test_get_todo_found(client_and_gateway):
    client, mock_gateway = client_and_gateway
    todo = ToDo(id=1, userId=1, title="Start Learning", completed=True)

    mock_gateway.get.return_value = todo

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == todo.model_dump()
    mock_gateway.get.assert_awaited_once_with(1)


def test_get_user_not_found(client_and_gateway):
    client, mock_gateway = client_and_gateway
    mock_gateway.get.return_value = None

    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo Not Found"
    mock_gateway.get.assert_awaited_once_with(999)
