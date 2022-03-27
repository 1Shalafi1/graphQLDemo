from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.actor import Actor
from app.schema.actor import ActorInput, ActorOutput, ActorOutputEnriched
from app.schema.film import FilmInput

actor_router = APIRouter()


@actor_router.get("/", tags=['actors'], response_model=List[ActorOutputEnriched] | List[ActorOutput])
def _list(skip: int = 0, limit: int = 10, enrich: bool = False, db: DbSession = Depends(get_db)):
    db_actors = Actor.get_list(db=db, skip=skip, limit=limit)
    if enrich is True:
        return [ActorOutputEnriched.from_orm(actor) for actor in db_actors]
    return [ActorOutput.from_orm(actor) for actor in db_actors]


@actor_router.put('{actor_id}/films', tags=['actors'], response_model=ActorOutputEnriched)
def assign_films(actor_id: int, films_data: Optional[List[FilmInput]] = None, films_ids: Optional[List[int]] = None,
                 db: DbSession = Depends(get_db)):
    return Actor.add_actor_films(db=db, actor_id=actor_id, films_data=films_data, films_ids=films_ids)


@actor_router.get('/{actor_id}', tags=['actors'], response_model=ActorOutputEnriched | ActorOutput)
def retrieve(actor_id: int, enrich: bool = False, db: DbSession = Depends(get_db)):
    db_actor = Actor.get_by_id(db=db, actor_id=actor_id)
    if enrich:
        return ActorOutputEnriched.from_orm(db_actor)
    return ActorOutput.from_orm(db_actor)


@actor_router.post('/', tags=['actors'], response_model=ActorOutput)
def create(actor: ActorInput, db: DbSession = Depends(get_db)):
    return Actor.create(data=actor, db=db)


@actor_router.put('/{actor_id}', tags=['actors'], response_model=ActorOutput)
def update(actor_id: int, actor: ActorInput, db: DbSession = Depends(get_db)):
    return Actor.update(data=actor, actor_id=actor_id, db=db)
