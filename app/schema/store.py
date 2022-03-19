from datetime import datetime

from app.schema.base import AbstractSchema


class StoreBase(AbstractSchema):
    address_id: int
    manager_staff_id: int

    class Config:
        orm_mode = True


class StoreInput(StoreBase):
    pass


class StoreOutput(StoreBase):
    store_id: int
    last_update: datetime
