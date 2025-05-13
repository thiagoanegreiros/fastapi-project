from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    title: str
    poster_path: str
    release_date: str
    overview: str

    model_config = {"from_attributes": True}
