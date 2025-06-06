import os
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.sessions import SessionMiddleware

from adapters.inbound.auth import require_auth
from adapters.inbound.routes import user_router
from domain.user import User
from infrastructure.container import Container
from infrastructure.logger.logger import Logger
from infrastructure.logger.logger_middleware import RequestLoggingMiddleware


@pytest.fixture
def client_and_repo():
    container = Container()

    # ✅ Mock assíncrono
    mock_repo = MagicMock()
    mock_repo.save = AsyncMock()
    mock_repo.get = AsyncMock()
    mock_repo.find_all = AsyncMock()
    mock_repo.delete = AsyncMock()

    mock_logger = MagicMock(spec=Logger)

    container.user_repository.override(mock_repo)
    container.logger.override(mock_logger)
    container.wire(
        modules=[
            "adapters.inbound.routes.user_router",
            "infrastructure.logger.logger_middleware",
        ]
    )

    app = FastAPI()

    secret_key = os.getenv("SECRET_KEY", "TEST_SECRET")
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SessionMiddleware, secret_key=secret_key)
    app.dependency_overrides[require_auth] = lambda: {"email": "test@example.com"}

    app.container = container
    app.include_router(user_router.router)

    client = TestClient(app, raise_server_exceptions=True)

    return client, mock_repo


def test_create_user(client_and_repo):
    client, mock_repo = client_and_repo
    user_input = {"name": "Test", "email": "test@example.com"}
    user_output = User(id="123", name="Test", email="test@example.com")

    mock_repo.save.return_value = user_output

    response = client.post("/users/", json=user_input)

    assert response.status_code == 200
    assert response.json() == user_output.model_dump()
    mock_repo.save.assert_awaited_once()


def test_list_users(client_and_repo):
    client, mock_repo = client_and_repo
    user1 = User(id="1", name="Alice", email="alice@example.com")
    user2 = User(id="2", name="Bob", email="bob@example.com")
    mock_repo.find_all.return_value = [user1, user2]

    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [user1.model_dump(), user2.model_dump()]
    mock_repo.find_all.assert_awaited_once()


def test_get_user_found(client_and_repo):
    client, mock_repo = client_and_repo
    user = User(id="1", name="Alice", email="alice@example.com")
    mock_repo.get.return_value = user

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == user.model_dump()
    mock_repo.get.assert_awaited_once_with("1")


def test_get_user_not_found(client_and_repo):
    client, mock_repo = client_and_repo
    mock_repo.get.return_value = None

    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"
    mock_repo.get.assert_awaited_once_with("999")


def test_delete_user_success(client_and_repo):
    client, mock_repo = client_and_repo
    mock_repo.delete.return_value = True

    response = client.delete("/users/123")
    assert response.status_code == 200
    mock_repo.delete.assert_awaited_once_with("123")


def test_delete_user_not_found(client_and_repo):
    client, mock_repo = client_and_repo
    mock_repo.delete.return_value = False

    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"
    mock_repo.delete.assert_awaited_once_with("999")


def test_update_user_success(client_and_repo):
    client, mock_repo = client_and_repo
    user_id = "123"
    user_input = {"name": "Updated Name", "email": "updated@example.com"}
    updated_user = User(id=user_id, name="Updated Name", email="updated@example.com")

    mock_repo.update = AsyncMock(return_value=updated_user)

    response = client.put(f"/users/{user_id}", json=user_input)

    assert response.status_code == 200
    assert response.json() == updated_user.model_dump()
    mock_repo.update.assert_awaited_once_with(user_id, user_input)


def test_update_user_not_found(client_and_repo):
    client, mock_repo = client_and_repo
    user_id = "999"
    user_input = {"name": "Not Found", "email": "notfound@example.com"}

    mock_repo.update = AsyncMock(return_value=None)

    response = client.put(f"/users/{user_id}", json=user_input)

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"
    mock_repo.update.assert_awaited_once_with(user_id, user_input)
