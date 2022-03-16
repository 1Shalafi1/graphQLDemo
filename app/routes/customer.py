from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.customer import Customer
from app.schema.customer import CustomerOutput, CustomerInput

customer_router = APIRouter()


@customer_router.get("/customer/", tags=['Customer'], response_model=List[CustomerOutput])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Customer.get_list(db=db, skip=skip, limit=limit)


@customer_router.get('/customer/{customer_id}', tags=['Customer'], response_model=CustomerOutput)
def retrieve(customer_id: int, db: DbSession = Depends(get_db)):
    return Customer.get_by_id(db=db, customer_id=customer_id)


@customer_router.post('/customer', tags=['Customer'], response_model=CustomerOutput)
def create(customer: CustomerInput, db: DbSession = Depends(get_db)):
    return Customer.create(data=customer, db=db)


@customer_router.put('/customer/{customer_id}', tags=['Customer'], response_model=CustomerOutput)
def update(customer_id: int, customer: CustomerInput, db: DbSession = Depends(get_db)):
    return Customer.update(data=customer, customer_id=customer_id, db = db)
