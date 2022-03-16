from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.actor import Actor
from app.schema.actor import ActorBase, ActorInput

actor_router = APIRouter()


@actor_router.get("/", tags=['actors'], response_model=List[ActorBase])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Actor.get_list(db=db, skip=skip, limit=limit)


@actor_router.get('/{actor_id}', tags=['actors'], response_model=ActorBase)
def retrieve(actor_id: int, db: DbSession = Depends(get_db)):
    return Actor.get_by_id(db=db, actor_id=actor_id)


@actor_router.post('/', tags=['actors'], response_model=ActorBase)
def create(actor: ActorInput, db: DbSession = Depends(get_db)):
    return Actor.create(data=actor, db=db)


@actor_router.put('/{actor_id}', tags=['actors'], response_model=ActorBase)
def update(actor_id: int, actor: ActorInput, db: DbSession = Depends(get_db)):
    return Actor.update(data=actor, actor_id=actor_id, db = db)
