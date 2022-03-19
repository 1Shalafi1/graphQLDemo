from datetime import datetime

from app.schema.base import AbstractSchema


class CustomerBase(AbstractSchema):
    address_id: int
    store_id: int
    first_name: str
    last_name: str
    email: str
    active: bool

    class Config:
        orm_mode = True


class CustomerInput(CustomerBase):
    pass


class CustomerOutput(CustomerBase):
    customer_id: int
    create_date: datetime
    last_update: datetime
