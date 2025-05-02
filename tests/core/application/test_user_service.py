from unittest.mock import AsyncMock, MagicMock

import pytest

from core.application.user_service import UserService
from core.domain.user import User


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.save = AsyncMock()
    repo.find_all = AsyncMock()
    repo.delete = AsyncMock()
    repo.get = AsyncMock()
    return repo


@pytest.fixture
def mock_logger():
    return MagicMock()


@pytest.fixture
def user_service(mock_repo, mock_logger):
    return UserService(user_repository=mock_repo, logger=mock_logger)


@pytest.mark.asyncio
async def test_create_user(user_service, mock_repo):
    user = User(id="id_01", name="Test User", email="test@example.com")
    mock_repo.save.return_value = user

    result = await user_service.save(user)

    mock_repo.save.assert_awaited_once_with(user)
    assert result == user


@pytest.mark.asyncio
async def test_list_users(user_service, mock_repo):
    users = [
        User(id="id_01", name="Alice", email="alice@email.com"),
        User(id="id_02", name="Bob", email="bob@email.com"),
    ]
    mock_repo.find_all.return_value = users

    result = await user_service.find_all()

    mock_repo.find_all.assert_awaited_once()
    assert result == users


@pytest.mark.asyncio
async def test_delete_user(user_service, mock_repo):
    mock_repo.delete.return_value = True

    result = await user_service.delete("id_01")

    mock_repo.delete.assert_awaited_once_with("id_01")
    assert result is True


@pytest.mark.asyncio
async def test_get_user(user_service, mock_repo):
    user = User(id="id_02", name="Bob", email="bob@email.com")
    mock_repo.get.return_value = user

    result = await user_service.get("id_02")

    mock_repo.get.assert_awaited_once_with("id_02")
    assert result == user
