from datetime import datetime

from app.schema.base import AbstractSchema


class CityBase(AbstractSchema):
    country_id: int
    city: str

    class Config:
        orm_mode = True


class CityInput(CityBase):
    pass


class CityOutput(CityBase):
    city_id: int
    last_update: datetime
