from datetime import datetime

from app.schema.base import AbstractSchema


class CountryBase(AbstractSchema):
    country: str

    class Config:
        orm_mode = True


class CountryInput(CountryBase):
    pass


class CountryOutput(CountryBase):
    country_id: int
    last_update: datetime
