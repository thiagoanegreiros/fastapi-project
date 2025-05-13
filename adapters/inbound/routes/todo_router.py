from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from application.todo_service import TodoService
from infrastructure.container import Container

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/")
@inject
async def list_todos(service: TodoService = Depends(Provide[Container.todo_service])):
    return await service.find_all()


@router.get("/{todo_id}")
@inject
async def get_todo(
    todo_id: int, service: TodoService = Depends(Provide[Container.todo_service])
):
    user = await service.get(todo_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return user
