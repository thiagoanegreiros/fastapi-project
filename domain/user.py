from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: Optional[str] = None

    model_config = {"from_attributes": True}
