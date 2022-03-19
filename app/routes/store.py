from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.store import Store
from app.schema.store import StoreOutput, StoreInput

store_router = APIRouter()


@store_router.get("/", tags=['Stores'], response_model=List[StoreOutput])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Store.get_list(db=db, skip=skip, limit=limit)


@store_router.get('/{store_id}', tags=['Stores'], response_model=StoreOutput)
def retrieve(store_id: int, db: DbSession = Depends(get_db)):
    return Store.get_by_id(db=db, obj_id=store_id)


@store_router.post('/', tags=['Stores'], response_model=StoreOutput)
def create(store: StoreInput, db: DbSession = Depends(get_db)):
    return Store.create(data=store, db=db)


@store_router.put('/{store_id}', tags=['Stores'], response_model=StoreOutput)
def update(store_id: int, store: StoreInput, db: DbSession = Depends(get_db)):
    return Store.update(data=store, obj_id=store_id, db=db)
