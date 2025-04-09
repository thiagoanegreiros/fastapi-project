import os
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.sessions import SessionMiddleware

from api.routes import user_router
from core.auth import require_auth
from core.container import Container
from core.domain.user import User
from core.logger.logger import Logger
from core.logger.logger_middleware import RequestLoggingMiddleware


@pytest.fixture
def client_and_repo():
    container = Container()

    mock_repo = MagicMock()
    mock_logger = MagicMock(spec=Logger)

    container.user_repository.override(mock_repo)
    container.logger.override(mock_logger)
    container.wire(modules=["api.routes.user_router", "core.logger.logger_middleware"])

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
    mock_repo.save.assert_called_once()


def test_list_users(client_and_repo):
    client, mock_repo = client_and_repo
    user1 = User(id="1", name="Alice", email="alice@example.com")
    user2 = User(id="2", name="Bob", email="bob@example.com")
    mock_repo.find_all.return_value = [user1, user2]

    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [user1.model_dump(), user2.model_dump()]
    mock_repo.find_all.assert_called_once()


def test_get_user_found(client_and_repo):
    client, mock_repo = client_and_repo
    user = User(id="1", name="Alice", email="alice@example.com")
    mock_repo.get.return_value = user

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == user.model_dump()
    mock_repo.get.assert_called_once_with("1")


def test_get_user_not_found(client_and_repo):
    client, mock_repo = client_and_repo
    mock_repo.get.return_value = None

    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"
    mock_repo.get.assert_called_once_with("999")


def test_delete_user_success(client_and_repo):
    client, mock_repo = client_and_repo
    mock_repo.delete.return_value = True

    response = client.delete("/users/123")
    assert response.status_code == 200
    mock_repo.delete.assert_called_once_with("123")


def test_delete_user_not_found(client_and_repo):
    client, mock_repo = client_and_repo
    mock_repo.delete.return_value = False

    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"
    mock_repo.delete.assert_called_once_with("999")
