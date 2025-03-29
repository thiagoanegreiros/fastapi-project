from unittest.mock import MagicMock

import pytest
from sqlmodel import Session

from core.domain.user import User
from infrastructure.database.models import UserDB
from infrastructure.database.user_repository import UserRepository


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


@pytest.fixture
def user_repository(mock_session):
    return UserRepository(mock_session)


def test_get_user(user_repository, mock_session):
    user_id = "123"
    fake_user_db = UserDB(id=user_id, name="John Doe", email="john@example.com")

    # Mockando retorno do get do SQLModel
    mock_session.get.return_value = fake_user_db

    result = user_repository.get(user_id)

    assert result.id == user_id
    assert result.name == "John Doe"
    mock_session.get.assert_called_once_with(UserDB, user_id)


def test_get_user_not_found(user_repository, mock_session):
    mock_session.get.return_value = None
    result = user_repository.get("not-found-id")
    assert result is None


def test_find_all_users(user_repository, mock_session):
    fake_users_db = [
        UserDB(id="1", name="Alice", email="alice@example.com"),
        UserDB(id="2", name="Bob", email="bob@example.com"),
    ]

    # Simulando a execução da query com exec().all()
    mock_exec = MagicMock()
    mock_exec.all.return_value = fake_users_db
    mock_session.exec.return_value = mock_exec

    result = user_repository.find_all()

    assert len(result) == 2
    assert result[0].name == "Alice"
    assert result[1].name == "Bob"
    mock_session.exec.assert_called_once()


def test_save_user(user_repository, mock_session):
    user = User(id="1", name="Alice", email="alice@example.com")
    UserDB(**user.model_dump())

    # Simular commit e refresh
    mock_session.refresh.side_effect = lambda x: None  # refresh não altera

    result = user_repository.save(user)

    # Testa se add, commit e refresh foram chamados corretamente
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert result.id == "1"
    assert result.name == "Alice"


def test_delete_user(user_repository, mock_session):
    user_id = "1"
    fake_user_db = UserDB(id=user_id, name="ToDelete", email="del@example.com")
    mock_session.get.return_value = fake_user_db

    result = user_repository.delete(user_id)

    assert result is True
    mock_session.commit.assert_called_once()


def test_delete_user_not_found(user_repository, mock_session):
    mock_session.get.return_value = None
    result = user_repository.delete("not-exist")
    assert result is False
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()
