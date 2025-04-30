from unittest.mock import Mock

import pytest

from core.application.movie_service import MovieService
from core.domain.movie import Movie


@pytest.fixture
def mock_gateway():
    return Mock()


@pytest.fixture
def mock_logger():
    return Mock()


@pytest.fixture
def movie_service(mock_gateway, mock_logger):
    return MovieService(gateway=mock_gateway, logger=mock_logger)


def test_find_all(movie_service, mock_gateway):
    # Arrange
    movies = [
        Movie(
            id=1,
            title="Matrix",
            poster_path="url1",
            overview="Neo",
            release_date="1999-03-31",
        ),
        Movie(
            id=2,
            title="Inception",
            poster_path="url2",
            overview="Dream",
            release_date="2010-07-16",
        ),
    ]
    mock_gateway.find_all.return_value = movies

    # Act
    result = movie_service.find_all("matrix")

    # Assert
    mock_gateway.find_all.assert_called_once_with("matrix")
    assert result == movies


def test_popular(movie_service, mock_gateway):
    # Arrange
    movies = [
        Movie(
            id=1,
            title="Popular Movie",
            poster_path="url",
            overview="Famous",
            release_date="2024-01-01",
        ),
    ]
    mock_gateway.popular.return_value = movies

    # Act
    result = movie_service.popular()

    # Assert
    mock_gateway.popular.assert_called_once()
    assert result == movies


def test_get_found(movie_service, mock_gateway):
    # Arrange
    movie = Movie(
        id=1,
        title="Matrix",
        poster_path="url",
        overview="Neo",
        release_date="1999-03-31",
    )
    mock_gateway.get.return_value = movie

    # Act
    result = movie_service.get(1)

    # Assert
    mock_gateway.get.assert_called_once_with(1)
    assert result == movie


def test_get_not_found(movie_service, mock_gateway):
    # Arrange
    mock_gateway.get.return_value = None

    # Act
    result = movie_service.get(999)

    # Assert
    mock_gateway.get.assert_called_once_with(999)
    assert result is None
