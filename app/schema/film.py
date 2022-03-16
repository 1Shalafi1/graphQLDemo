import decimal
from datetime import datetime
from typing import List

from app.schema.base import AbstractSchema


class FilmBase(AbstractSchema):
    language_id: int

    title: str
    description: str
    release_year: datetime
    rental_duration: int
    rental_rate: int
    length: int
    replacement_cost: decimal.Decimal
    rating: str

    special_features: List[str]

    fulltext: str

    class Config:
        orm_mode = True


class FilmInput(FilmBase):
    pass


class FilmOutput(FilmBase):
    film_id: int
    film_update: datetime
