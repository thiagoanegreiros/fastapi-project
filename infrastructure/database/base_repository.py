from typing import Generic, List, Type, TypeVar

from sqlmodel import Session, select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get(self, id: str) -> T | None:
        return self.session.get(self.model, id)

    def find_all(self) -> List[T]:
        return self.session.exec(select(self.model)).all()

    def save(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, id: str) -> bool:
        obj = self.get(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False
