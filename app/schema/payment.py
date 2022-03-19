import decimal
from datetime import datetime

from app.schema.base import AbstractSchema


class PaymentBase(AbstractSchema):
    customer_id: int
    staff_id: int
    rental_id: int

    amount: decimal.Decimal

    class Config:
        orm_mode = True


class PaymentInput(PaymentBase):
    pass


class PaymentOutput(PaymentBase):
    payment_id: int
    payment_date: datetime
