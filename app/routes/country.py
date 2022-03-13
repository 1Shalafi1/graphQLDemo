from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.country import Country
from app.schema.country import CountryInput, CountryOutput

country_router = APIRouter()


@country_router.get("/country/", tags=['Countries'], response_model=List[CountryOutput])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Country.get_list(db=db, skip=skip, limit=limit)


@country_router.get('/country/{country_id}', tags=['Countries'], response_model=CountryOutput)
def retrieve(country_id: int, db: DbSession = Depends(get_db)):
    return Country.get_by_id(db=db, obj_id=country_id)


@country_router.post('/country', tags=['Countries'], response_model=CountryOutput)
def create(country: CountryInput, db: DbSession = Depends(get_db)):
    return Country.create(data=country, db=db)


@country_router.post('/country/{country_id}', tags=['Countries'], response_model=CountryOutput)
def update(country_id: int, country: CountryInput, db: DbSession = Depends(get_db)):
    return Country.update(data=country, obj_id=country_id, db=db)
