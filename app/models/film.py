from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import ForeignKey, VARCHAR, Text, Numeric, String, ARRAY
from sqlalchemy import Integer, Column, TIMESTAMP, Index
from sqlalchemy.orm import Session as DbSession, relationship

from app.database import Base
from app.models.__relations_tables import film_actor, film_category
from app.schema.film import FilmOutput, FilmInput


class Film(Base):
    __tablename__ = 'film'
    __table_args__ = (
        Index('film_pkey', 'film_id'),
        Index('film_fulltext_idx', 'fulltext'),
        Index('idx_fk_language_id', 'language_id'),
        Index('idx_title', 'title'),
    )

    film_id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    language_id = Column(Integer, ForeignKey('language.language_id', name='film_language_id_fkey'))

    title = Column(VARCHAR(255))
    description = Column(Text)
    release_year = Column(TIMESTAMP)
    rental_duration = Column(Integer)
    rental_rate = Column(Numeric)
    length = Column(Integer)
    replacement_cost = Column(Numeric)
    rating = Column(Text)
    special_features = Column(ARRAY(String))
    fulltext = Column(String)

    last_update = Column(TIMESTAMP)

    actors = relationship('Actor', secondary=film_actor)
    categories = relationship('Category', secondary=film_category)

    @classmethod
    def create(cls, db: DbSession, data: FilmInput) -> FilmOutput:
        new_obj = cls(
            **data.dict(),
            last_update=datetime.utcnow(),
        )
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)

        return new_obj

    @classmethod
    def get_list(cls, db: DbSession, limit: int = 10, skip: int = 0) -> List[FilmOutput]:
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: DbSession, film_id: int) -> FilmOutput:
        return db.query(cls).filter(cls.film_id == film_id).first()

    @classmethod
    def update(cls, db: DbSession, film_id: int, data: FilmInput) -> FilmOutput:
        db_object = cls.get_by_id(db=db, film_id=film_id)
        if not db_object:
            raise HTTPException(status_code=404, detail='Address not found')

        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_object, key, value)
        db_object.last_update = datetime.utcnow()
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

        return db_object
