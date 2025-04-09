from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request

from core.application.user_service import UserService
from core.container import Container
from core.domain.user import User
from core.logger.logger_middleware import log_with_request

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
@inject
def create_user(
    request: Request,
    user: User,
    service: UserService = Depends(Provide[Container.user_service]),
):
    del user.id
    log_with_request(
        request, data={"event": "Usuário criado com sucesso", "user": "fulano"}
    )

    return service.save(user)


@router.get("/")
@inject
def list_users(service: UserService = Depends(Provide[Container.user_service])):
    return service.find_all()


@router.delete("/{user_id}")
@inject
def delete_user(
    user_id: str, service: UserService = Depends(Provide[Container.user_service])
):
    if service.delete(user_id) is False:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


@router.get("/{user_id}")
@inject
def get_user(
    user_id: str, service: UserService = Depends(Provide[Container.user_service])
):
    user = service.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
