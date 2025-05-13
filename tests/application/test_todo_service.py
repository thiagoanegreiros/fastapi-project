from unittest.mock import AsyncMock, Mock

import pytest

from application.todo_service import TodoService
from domain.todo import ToDo


@pytest.fixture
def mock_gateway():
    gateway = Mock()
    gateway.find_all = AsyncMock()
    gateway.get = AsyncMock()
    return gateway


@pytest.fixture
def mock_logger():
    return Mock()


@pytest.fixture
def todo_service(mock_gateway, mock_logger):
    return TodoService(gateway=mock_gateway, logger=mock_logger)


@pytest.mark.asyncio
async def test_find_all(todo_service, mock_gateway):
    # Arrange
    todos = [
        ToDo(id=1, userId=1, title="Comprar pão", completed=False),
        ToDo(id=2, userId=1, title="Estudar Python", completed=True),
    ]
    mock_gateway.find_all.return_value = todos

    # Act
    result = await todo_service.find_all()

    # Assert
    mock_gateway.find_all.assert_awaited_once()
    assert result == todos


@pytest.mark.asyncio
async def test_get(todo_service, mock_gateway):
    # Arrange
    todo = ToDo(id=1, userId=1, title="Comprar pão", completed=False)
    mock_gateway.get.return_value = todo

    # Act
    result = await todo_service.get(1)

    # Assert
    mock_gateway.get.assert_awaited_once_with(1)
    assert result == todo


@pytest.mark.asyncio
async def test_get_not_found(todo_service, mock_gateway):
    # Arrange
    mock_gateway.get.return_value = None

    # Act
    result = await todo_service.get(999)

    # Assert
    mock_gateway.get.assert_awaited_once_with(999)
    assert result is None
