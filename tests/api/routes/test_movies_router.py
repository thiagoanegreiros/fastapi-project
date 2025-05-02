from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routes import movies_router
from core.auth import require_auth
from core.container import Container
from core.domain.movie import Movie
from core.logger.logger import Logger
from core.logger.logger_middleware import RequestLoggingMiddleware


@pytest.fixture
def client_and_service():
    container = Container()

    # ✅ Mocks assíncronos
    mock_service = MagicMock()
    mock_service.find_all = AsyncMock()
    mock_service.get = AsyncMock()
    mock_service.popular = AsyncMock()

    mock_logger = MagicMock(spec=Logger)

    container.movie_service.override(mock_service)
    container.logger.override(mock_logger)
    container.wire(
        modules=["api.routes.movies_router", "core.logger.logger_middleware"]
    )

    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    app.dependency_overrides[require_auth] = lambda: {"email": "test@example.com"}

    app.container = container
    app.include_router(movies_router.router)

    client = TestClient(app, raise_server_exceptions=True)
    return client, mock_service


def test_list_movies(client_and_service):
    client, mock_service = client_and_service
    movie1 = Movie(
        id=1,
        title="The Matrix",
        poster_path="url1",
        overview="Test",
        release_date="1999-03-31",
    )
    movie2 = Movie(
        id=2,
        title="Inception",
        poster_path="url2",
        overview="Dreams",
        release_date="2010-07-16",
    )

    mock_service.find_all.return_value = [movie1, movie2]

    response = client.get("/movies/search/matrix")
    assert response.status_code == 200
    assert response.json() == [movie1.model_dump(), movie2.model_dump()]
    mock_service.find_all.assert_awaited_once_with(query="matrix")


def test_popular_movies(client_and_service):
    client, mock_service = client_and_service
    movie = Movie(
        id=3,
        title="Interstellar",
        poster_path="url3",
        overview="Space travel",
        release_date="2014-11-07",
    )

    mock_service.popular.return_value = [movie]

    response = client.get("/movies/popular")
    assert response.status_code == 200
    assert response.json() == [movie.model_dump()]
    mock_service.popular.assert_awaited_once()


def test_get_movie_found(client_and_service):
    client, mock_service = client_and_service
    movie = Movie(
        id=1,
        title="The Matrix",
        poster_path="url",
        overview="Neo",
        release_date="1999-03-31",
    )

    mock_service.get.return_value = movie

    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json() == movie.model_dump()
    mock_service.get.assert_awaited_once_with(1)


def test_get_movie_not_found(client_and_service):
    client, mock_service = client_and_service
    mock_service.get.return_value = None

    response = client.get("/movies/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie Not Found"
    mock_service.get.assert_awaited_once_with(999)
