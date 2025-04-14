from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from core.application.todo_service import TodoService
from core.container import Container

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/")
@inject
def list_todos(service: TodoService = Depends(Provide[Container.todo_service])):
    return service.find_all()


@router.get("/{todo_id}")
@inject
def get_todo(
    todo_id: int, service: TodoService = Depends(Provide[Container.todo_service])
):
    user = service.get(todo_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Not Found Todo")
    return user
