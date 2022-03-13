from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.address import Address
from app.schema.address import AddressOutput, AddressInput

address_router = APIRouter()


@address_router.get("/Addresses/", tags=['Addresses'], response_model=List[AddressOutput])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Address.get_list(db=db, skip=skip, limit=limit)


@address_router.get('/address/{address_id}', tags=['Addresses'], response_model=AddressOutput)
def retrieve(address_id: int, db: DbSession = Depends(get_db)):
    return Address.get_by_id(db=db, address_id=address_id)


@address_router.post('/address', tags=['Addresses'], response_model=AddressOutput)
def create(address: AddressInput, db: DbSession = Depends(get_db)):
    return Address.create(data=address, db=db)


@address_router.post('/address/{address_id}', tags=['Addresses'], response_model=AddressOutput)
def update(address_id: int, address: AddressInput, db: DbSession = Depends(get_db)):
    return Address.update(data=address, address_id=address_id, db = db)
