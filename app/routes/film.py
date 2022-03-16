from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.film import Film
from app.schema.film import FilmBase, FilmInput

film_router = APIRouter()


@film_router.get("/", tags=['film'], response_model=List[FilmBase])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Film.get_list(db=db, skip=skip, limit=limit)


@film_router.get('/{film_id}', tags=['film'], response_model=FilmBase)
def retrieve(film_id: int, db: DbSession = Depends(get_db)):
    return Film.get_by_id(db=db, film_id=film_id)


@film_router.post('/', tags=['film'], response_model=FilmBase)
def create(film: FilmInput, db: DbSession = Depends(get_db)):
    return Film.create(data=film, db=db)


@film_router.put('/{film_id}', tags=['film'], response_model=FilmBase)
def update(film_id: int, film: FilmInput, db: DbSession = Depends(get_db)):
    return Film.update(data=film, film_id=film_id, db = db)
