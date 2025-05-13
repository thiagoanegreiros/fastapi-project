from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import HTTPStatusError, Request, Response

from adapters.out.api.movies_api_client import MoviesApiClient
from domain.movie import Movie


@pytest.fixture
def client():
    return MoviesApiClient(base_url="https://fakeapi.com")


@pytest.mark.asyncio
async def test_find_all(client):
    movies_data = {
        "results": [
            {
                "id": 1,
                "title": "Matrix",
                "poster_path": "/poster1.jpg",
                "overview": "Neo",
                "release_date": "1999-03-31",
            },
            {
                "id": 2,
                "title": "Inception",
                "poster_path": "/poster2.jpg",
                "overview": "Dream",
                "release_date": "2010-07-16",
            },
        ]
    }

    mock_response = MagicMock()
    mock_response.json.return_value = movies_data
    mock_response.raise_for_status.return_value = None

    with patch(
        "httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)
    ) as mock_get:
        result = await client.find_all("matrix")

        mock_get.assert_called_once_with(
            "https://fakeapi.com/search/movie",
            headers=client.headers,
            params={"query": "matrix"},
        )

        expected = [
            Movie.model_validate(
                {
                    **m,
                    "poster_path": f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{m['poster_path']}",
                }
            )
            for m in movies_data["results"]
        ]
        assert len(result) == len(expected)


@pytest.mark.asyncio
async def test_popular(client):
    movies_data = {
        "results": [
            {
                "id": 1,
                "title": "Popular Movie",
                "poster_path": "/popular.jpg",
                "overview": "Overview",
                "release_date": "2024-01-01",
            },
        ]
    }

    mock_response = MagicMock()
    mock_response.json.return_value = movies_data
    mock_response.raise_for_status.return_value = None

    with patch(
        "httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)
    ) as mock_get:
        result = await client.popular()

        mock_get.assert_called_once_with(
            "https://fakeapi.com/movie/popular", headers=client.headers
        )
        assert result == [
            Movie.model_validate(
                {
                    **movies_data["results"][0],
                    "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/popular.jpg",
                }
            )
        ]


@pytest.mark.asyncio
async def test_get(client):
    movie_data = {
        "id": 1,
        "title": "Matrix",
        "poster_path": "/matrix.jpg",
        "overview": "Neo saves the world",
        "release_date": "1999-03-31",
    }

    mock_response = MagicMock()
    mock_response.json.return_value = movie_data
    mock_response.raise_for_status.return_value = None

    with patch(
        "httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)
    ) as mock_get:
        result = await client.get(1)

        mock_get.assert_called_once_with(
            "https://fakeapi.com/movie/1", headers=client.headers
        )

        expected = Movie.model_validate(
            {
                **movie_data,
                "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/matrix.jpg",
            }
        )
        assert result == expected


@pytest.mark.asyncio
async def test_find_all_http_error(client):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPStatusError(
        "Error",
        request=Request("GET", "https://fakeapi.com/search/movie"),
        response=Response(500),
    )

    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)):
        with pytest.raises(HTTPStatusError):
            await client.find_all("matrix")


@pytest.mark.asyncio
async def test_popular_http_error(client):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPStatusError(
        "Error",
        request=Request("GET", "https://fakeapi.com/movie/popular"),
        response=Response(500),
    )

    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)):
        with pytest.raises(HTTPStatusError):
            await client.popular()


@pytest.mark.asyncio
async def test_get_http_error(client):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPStatusError(
        "Error",
        request=Request("GET", "https://fakeapi.com/movie/1"),
        response=Response(404),
    )

    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)):
        with pytest.raises(HTTPStatusError):
            await client.get(1)


@pytest.mark.asyncio
async def test_find_all_without_poster_path(client):
    movies_data = {
        "results": [
            {
                "id": 3,
                "title": "Posterless Movie",
                "overview": "No poster here",
                "release_date": "2020-01-01",
                "poster_path": None,
            },
        ]
    }

    mock_response = MagicMock()
    mock_response.json.return_value = movies_data
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)):
        result = await client.find_all("posterless")
        assert len(result) == 1
        assert result[0].title == "Posterless Movie"


@pytest.mark.asyncio
async def test_get_without_poster_path(client):
    movie_data = {
        "id": 99,
        "title": "The Hidden Poster",
        "overview": "No image here",
        "release_date": "2021-12-12",
        "poster_path": None,
    }

    mock_response = MagicMock()
    mock_response.json.return_value = movie_data
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)):
        result = await client.get(99)
        assert result.title == "The Hidden Poster"
