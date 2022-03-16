from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.payment import Payment
from app.schema.payment import PaymentBase, PaymentInput

payment_router = APIRouter()


@payment_router.get("/", tags=['payments'], response_model=List[PaymentBase])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Payment.get_list(db=db, skip=skip, limit=limit)


@payment_router.get('/{payment_id}', tags=['payments'], response_model=PaymentBase)
def retrieve(payment_id: int, db: DbSession = Depends(get_db)):
    return Payment.get_by_id(db=db, payment_id=payment_id)


@payment_router.post('/', tags=['payments'], response_model=PaymentBase)
def create(payment: PaymentInput, db: DbSession = Depends(get_db)):
    return Payment.create(data=payment, db=db)


@payment_router.put('/{payment_id}', tags=['payments'], response_model=PaymentBase)
def update(payment_id: int, payment: PaymentInput, db: DbSession = Depends(get_db)):
    return Payment.update(data=payment, payment_id=payment_id, db = db)
