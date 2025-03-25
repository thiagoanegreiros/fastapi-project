from typing import Optional
import uuid
from sqlmodel import SQLModel, Field

class UserDB(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    email: Optional[str] = None
