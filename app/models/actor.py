from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import Integer, Column, String, TIMESTAMP, Index
from sqlalchemy.orm import Session as DbSession

from app.database import Base
from app.schema.actor import ActorInput

# SQlAlchemy models
class Actor(Base):
    __tablename__ = 'actor'
    __table_args__ = (
        Index('actor_pkey', "actor_id"),
        Index('idx_actor_last_name', "last_name"),
    )

    actor_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    last_update = Column(TIMESTAMP)

    @classmethod
    def get_actors_list(cls, db: DbSession, limit: int = 10, skip: int = 0, **filters):
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_actor_by_id(cls, db: DbSession, actor_id: int):
        return db.query(cls).filter(cls.actor_id == actor_id).first()

    @classmethod
    def set_actor(cls, db: DbSession, data: ActorInput):
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
    def update_actor(cls, db: DbSession, actor_id: int, data: ActorInput):
        db_actor = cls.get_actor_by_id(db=db, actor_id=actor_id)
        if not db_actor:
            raise HTTPException(status_code=404, detail='Actor not found')
        actor_data = data.dict(exclude_unset=True)
        for key, value in actor_data.items():
            setattr(db_actor, key, value)
        db_actor.last_update = datetime.utcnow()
        db.add(db_actor)
        db.commit()
        db.refresh(db_actor)

        return db_actor



# SQlAlchemy model extras
# TODO: Add triggers

