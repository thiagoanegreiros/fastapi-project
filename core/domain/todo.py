from pydantic import BaseModel


class ToDo(BaseModel):
    id: int
    userId: int
    title: str
    completed: bool

    model_config = {"from_attributes": True}
