from unittest.mock import AsyncMock, MagicMock

import pytest

from adapters.out.database.models import UserDB
from adapters.out.database.user_repository import UserRepository
from domain.user import User


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.get = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.update = AsyncMock()
    session.add = MagicMock()
    return session


@pytest.fixture
def user_repository(mock_session):
    return UserRepository(mock_session)


@pytest.mark.asyncio
async def test_get_user(user_repository, mock_session):
    user_id = "123"
    fake_user_db = UserDB(id=user_id, name="John Doe", email="john@example.com")
    mock_session.get.return_value = fake_user_db

    result = await user_repository.get(user_id)

    assert result.id == user_id
    assert result.name == "John Doe"
    mock_session.get.assert_awaited_once_with(UserDB, user_id)


@pytest.mark.asyncio
async def test_get_user_not_found(user_repository, mock_session):
    mock_session.get.return_value = None

    result = await user_repository.get("not-found-id")

    assert result is None
    mock_session.get.assert_awaited_once_with(UserDB, "not-found-id")


@pytest.mark.asyncio
async def test_find_all_users(user_repository, mock_session):
    fake_users_db = [
        UserDB(id="1", name="Alice", email="alice@example.com"),
        UserDB(id="2", name="Bob", email="bob@example.com"),
    ]

    mock_scalars = MagicMock()
    mock_scalars.all.return_value = fake_users_db  # ✅

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    mock_session.execute.return_value = mock_result

    result = await user_repository.find_all()

    assert len(result) == 2
    assert result[0].name == "Alice"
    assert result[1].name == "Bob"
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_user(user_repository, mock_session):
    user = User(id="1", name="Alice", email="alice@example.com")

    result = await user_repository.save(user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.id == "1"
    assert result.name == "Alice"


@pytest.mark.asyncio
async def test_delete_user(user_repository, mock_session):
    user_id = "1"
    fake_user_db = UserDB(id=user_id, name="ToDelete", email="del@example.com")
    mock_session.get.return_value = fake_user_db

    result = await user_repository.delete(user_id)

    assert result is True
    mock_session.get.assert_awaited_once_with(UserDB, user_id)
    mock_session.delete.assert_awaited_once()  # <- relaxa a verificação
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_not_found(user_repository, mock_session):
    mock_session.get.return_value = None

    result = await user_repository.delete("not-exist")

    assert result is False
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_update_user(user_repository, mock_session):
    user_id = "1"
    fake_user_db = UserDB(id=user_id, name="ToUpdate", email="del@example.com")
    mock_session.get.return_value = fake_user_db

    data = {"id": "1", "name": "UpdatedName", "email": "updated@example.com"}

    result = await user_repository.update(user_id, data)

    assert result == UserDB(id=user_id, name="UpdatedName", email="updated@example.com")
    mock_session.get.assert_awaited_once_with(UserDB, user_id)
    mock_session.commit.assert_awaited_once()
