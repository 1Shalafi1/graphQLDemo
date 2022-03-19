from datetime import datetime

from app.schema.base import AbstractSchema


class AddressBase(AbstractSchema):
    address: str
    address2: str
    district: str
    postal_code: str
    phone: str

    class Config:
        orm_mode = True


class AddressInput(AddressBase):
    pass


class AddressOutput(AddressBase):
    address_id: int
    last_update: datetime
