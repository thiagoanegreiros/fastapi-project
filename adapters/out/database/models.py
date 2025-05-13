import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


class UserDB(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    email: Optional[str] = None
