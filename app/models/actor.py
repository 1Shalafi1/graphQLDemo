from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import Integer, Column, String, TIMESTAMP, Index
from sqlalchemy.orm import Session as DbSession, relationship

from app.database import Base
from app.models.__relations_tables import film_actor
from app.schema.actor import ActorInput, ActorBase


# SQlAlchemy models
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
    def get_list(cls, db: DbSession, limit: int = 10, skip: int = 0) -> ActorBase:
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
