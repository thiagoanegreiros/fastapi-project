
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from core.application.user_service import UserService
from core.container import Container
from core.domain.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
@inject
def create_user(
    user: User, service: UserService = Depends(Provide[Container.user_service])
):
    return service.create_user(user)


@router.get("/")
@inject
def list_users(service: UserService = Depends(Provide[Container.user_service])):
    return service.list_users()

@router.delete("/{user_id}")
@inject
def delete_user(user_id: str, service: UserService = Depends(Provide[Container.user_service])):
    return service.delete_user(user_id)

@router.get("/{user_id}")
@inject
def get_user(user_id: str, service: UserService = Depends(Provide[Container.user_service])):
    user = service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
