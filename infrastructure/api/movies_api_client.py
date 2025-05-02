from typing import List, Optional

import httpx
from ta_envy import Env

from core.domain.movie import Movie
from core.domain.movie_api_client_interface import IMovieGateway

env = Env(required=["MOVIE_API_KEY"])


class MoviesApiClient(IMovieGateway):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {env.get('MOVIE_API_KEY')}",
            "Accept": "application/json",
        }

    def _process_movies(self, raw_data: dict) -> List[Movie]:
        results = []
        for movie_data in raw_data["results"]:
            if "poster_path" in movie_data:
                movie_data["poster_path"] = (
                    f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{movie_data['poster_path']}"
                )
            results.append(Movie.model_validate(movie_data))
        return results

    async def find_all(self, query: str) -> Optional[List[Movie]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/search/movie",
                headers=self.headers,
                params={"query": query},
            )
            response.raise_for_status()
            return self._process_movies(response.json())

    async def popular(self) -> Optional[List[Movie]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/movie/popular", headers=self.headers
            )
            response.raise_for_status()
            return self._process_movies(response.json())

    async def get(self, id: int) -> Movie:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/movie/{id}", headers=self.headers
            )
            response.raise_for_status()
            movie_data = response.json()

            if "poster_path" in movie_data:
                movie_data["poster_path"] = (
                    f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{movie_data['poster_path']}"
                )

            return Movie.model_validate(movie_data)
