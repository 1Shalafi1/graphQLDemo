from datetime import datetime
from typing import Optional

from app.schema.base import AbstractSchema


class StaffBase(AbstractSchema):
    address_id: int
    first_name: str
    last_name: str
    username: str
    active: bool
    picture: bytes

    class Config:
        orm_mode = True


class StaffInput(StaffBase):
    password: Optional[str]


class StaffCreate(StaffBase):
    password: str


class StaffOutput(StaffBase):
    staff_id: int
    last_update: datetime
