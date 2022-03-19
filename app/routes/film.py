from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.film import Film
from app.schema.film import FilmInput, FilmOutputEnriched, FilmOutput

film_router = APIRouter()


@film_router.get("/", tags=['film'], response_model=List[FilmOutputEnriched] | List[FilmOutput])
def _list(skip: int = 0, limit: int = 10, enrich: bool = False, db: DbSession = Depends(get_db)):
    db_films = Film.get_list(db=db, skip=skip, limit=limit)
    if enrich is True:
        return [FilmOutputEnriched.from_orm(film) for film in db_films]
    return [FilmOutput.from_orm(film) for film in db_films]


@film_router.get('/{film_id}', tags=['film'], response_model=FilmOutputEnriched | FilmOutput)
def retrieve(film_id: int, enrich: bool = False, db: DbSession = Depends(get_db)):
    db_film = Film.get_by_id(db=db, film_id=film_id)
    if enrich is True:
        return FilmOutputEnriched.from_orm(db_film)
    return FilmOutput.from_orm(db_film)


@film_router.post('/', tags=['film'], response_model=FilmOutput)
def create(film: FilmInput, db: DbSession = Depends(get_db)):
    return Film.create(data=film, db=db)


@film_router.put('/{film_id}', tags=['film'], response_model=FilmOutput)
def update(film_id: int, film: FilmInput, db: DbSession = Depends(get_db)):
    return Film.update(data=film, film_id=film_id, db=db)
