from strawberry.types import Info


async def list_todos(info: Info):
    service = info.context["todo_service"]
    return service.find_all()
