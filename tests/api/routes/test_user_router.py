import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from core.domain.user import User
from core.application.user_service import UserService
from core.container import Container
from api.routes import user_router


@pytest.fixture
def mock_user_service():
    return MagicMock(spec=UserService)


@pytest.fixture
def client(mock_user_service):
    container = Container()
    container.user_service.override(mock_user_service)

    container.wire(modules=[user_router])

    app = FastAPI()
    app.container = container
    app.include_router(user_router.router)

    return TestClient(app)


def test_create_user(client, mock_user_service):
    user_input = {"name": "Test", "email": "test@example.com"}
    user_output = User(id="123", name="Test", email="test@example.com")

    mock_user_service.save.return_value = user_output

    response = client.post("/users/", json=user_input)

    assert response.status_code == 200
    assert response.json() == user_output.model_dump()
    mock_user_service.save.assert_called_once()


def test_list_users(client, mock_user_service):
    user1 = User(id="1", name="Alice", email="alice@example.com")
    user2 = User(id="2", name="Bob", email="bob@example.com")
    mock_user_service.find_all.return_value = [user1, user2]

    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [user1.model_dump(), user2.model_dump()]
    mock_user_service.find_all.assert_called_once()


def test_get_user_found(client, mock_user_service):
    user = User(id="1", name="Alice", email="alice@example.com")
    mock_user_service.get.return_value = user

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == user.model_dump()
    mock_user_service.get.assert_called_once_with("1")


def test_get_user_not_found(client, mock_user_service):
    mock_user_service.get.return_value = None

    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"


def test_delete_user_success(client, mock_user_service):
    mock_user_service.delete.return_value = True

    response = client.delete("/users/123")
    assert response.status_code == 200
    mock_user_service.delete.assert_called_once_with("123")


def test_delete_user_not_found(client, mock_user_service):
    mock_user_service.delete.return_value = False

    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"
