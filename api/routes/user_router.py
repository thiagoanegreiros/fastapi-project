from fastapi import APIRouter, Depends
from core.application.user_service import UserService
from core.domain.user import User
from dependency_injector.wiring import inject, Provide
from core.container import Container

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
@inject
def create_user(user: User, service: UserService = Depends(Provide[Container.user_service])):
    return service.create_user(user)

@router.get("/")
@inject
def list_users(service: UserService = Depends(Provide[Container.user_service])):
    return service.list_users()
