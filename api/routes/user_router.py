from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request

from core.application.user_service import UserService
from core.auth import require_auth
from core.container import Container
from core.domain.user import User
from core.logger.logger_middleware import log_with_request

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", dependencies=[Depends(require_auth)])
@inject
async def create_user(
    request: Request,
    user: User,
    service: UserService = Depends(Provide[Container.user_service]),
):
    del user.id
    log_with_request(
        request, data={"event": "Usuário criado com sucesso", "user": "fulano"}
    )

    return await service.save(user)


@router.get("/", dependencies=[Depends(require_auth)])
@inject
async def list_users(service: UserService = Depends(Provide[Container.user_service])):
    return await service.find_all()


@router.delete("/{user_id}", dependencies=[Depends(require_auth)])
@inject
async def delete_user(
    user_id: str, service: UserService = Depends(Provide[Container.user_service])
):
    if await service.delete(user_id) is False:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


@router.get("/{user_id}", dependencies=[Depends(require_auth)])
@inject
async def get_user(
    user_id: str, service: UserService = Depends(Provide[Container.user_service])
):
    user = await service.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
