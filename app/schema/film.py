import decimal
from datetime import datetime
from enum import Enum
from typing import List, Optional

from app.schema.base import AbstractSchema
from app.schema.category import CategoryOutput

class MPPARatingEnum(str, Enum):
    G = 'G'
    PG = 'PG'
    PG13 = 'PG-13'
    R = 'R'
    NC17='NC-17'



class FilmBase(AbstractSchema):
    language_id: int

    title: str
    description: str
    release_year: str
    rental_duration: int
    rental_rate: int
    length: int
    replacement_cost: decimal.Decimal
    rating: MPPARatingEnum

    special_features: List[str] = []

    fulltext: str = ""

    class Config:
        orm_mode = True


class FilmInput(FilmBase):
    pass


class FilmOutput(FilmBase):
    film_id: int
    last_update: datetime


class FilmOutputWithCategories(FilmOutput):
    categories: List[CategoryOutput]


class FilmOutputEnriched(FilmOutput):
    from app.schema.actor import ActorOutput
    actors: List[ActorOutput]
    categories: List[CategoryOutput]
