from datetime import datetime
from typing import List

from app.schema.base import AbstractSchema


class ActorBase(AbstractSchema):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class ActorInput(ActorBase):
    pass


class ActorOutput(ActorBase):
    actor_id: int
    last_update: datetime


class ActorOutputEnriched(ActorOutput):
    from app.schema.film import FilmOutputWithCategories
    films: List[FilmOutputWithCategories]
