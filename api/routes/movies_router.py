from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from core.application.movie_service import MovieService
from core.auth import require_auth
from core.container import Container

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/search/{query}")
@inject
async def list_movies(
    query: str,
    service: MovieService = Depends(Provide[Container.movie_service]),
    _=Depends(require_auth),
):
    return await service.find_all(query=query)


@router.get("/popular")
@inject
async def popular(
    service: MovieService = Depends(Provide[Container.movie_service]),
    _=Depends(require_auth),
):
    return await service.popular()


@router.get("/{movie_id}")
@inject
async def get_movie(
    movie_id: int,
    service: MovieService = Depends(Provide[Container.movie_service]),
    _=Depends(require_auth),
):
    user = await service.get(movie_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Movie Not Found")
    return user
