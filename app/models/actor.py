import json
from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import Integer, Column, String, TIMESTAMP, Index
from sqlalchemy.orm import Session as DbSession, relationship

from app.database import Base
from app.models.__relations_tables import film_actor
from app.models.film import Film
from app.schema.actor import ActorInput, ActorBase
from app.schema.film import FilmInput


class Actor(Base):
    __tablename__ = 'actor'
    __table_args__ = (
        Index('actor_pkey', "actor_id"),
        Index('idx_actor_last_name', "last_name"),
    )

    actor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    last_update = Column(TIMESTAMP)

    films = relationship('Film', secondary=film_actor)

    @classmethod
    def get_list(cls, db: DbSession, limit: int = 10, skip: int = 0, **filters) -> ActorBase:
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: DbSession, actor_id: int) -> ActorBase:
        return db.query(cls).filter(cls.actor_id == actor_id).first()

    @classmethod
    def create(cls, db: DbSession, data: ActorInput) -> ActorBase:
        new_user = cls(
            first_name=data.first_name,
            last_name=data.last_name,
            last_update=datetime.utcnow()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @classmethod
    def add_actor_films(cls, db: DbSession, actor_id, films_data: Optional[List[FilmInput]] = None,
                        films_ids: List[int] = None):

        if not (films_ids or films_data):
            raise HTTPException(status_code=400, detail='New films object or films ids are required')

        films_data = [] if films_data is None else films_data
        films_ids = [] if films_ids is None else films_ids

        db_object = cls.get_by_id(db, actor_id)
        if not db_object:
            raise HTTPException(status_code=404, detail='Actor not found')

        errors = []
        films = []

        for film in films_data:
            try:
                films.append(Film.create(db, film))
            except Exception as err:
                errors.append({'object': film, 'details': str(err)})

        if errors:
            raise HTTPException(status_code=400, detail=json.dumps(errors))

        if films_ids:
            films.extend(Film.get_list_by_id(db, films_ids))

        db_object.films = films
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

        return db_object

    @classmethod
    def update(cls, db: DbSession, actor_id: int, data: ActorInput) -> ActorBase:
        db_object = cls.get_by_id(db=db, actor_id=actor_id)
        if not db_object:
            raise HTTPException(status_code=404, detail='Actor not found')

        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_object, key, value)
        db_object.last_update = datetime.utcnow()
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

        return db_object

# SQlAlchemy model extras
# TODO: Add triggers
