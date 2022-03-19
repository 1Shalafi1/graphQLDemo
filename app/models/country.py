from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import Integer, Column, TIMESTAMP, Index, VARCHAR
from sqlalchemy.orm import Session as DbSession

from app.database import Base
from app.schema.country import CountryInput, CountryOutput


class Country(Base):
    __tablename__ = 'country'
    __table_args__ = (
        Index('country_pkey', 'country_id'),
    )

    country_id = Column(Integer, primary_key=True, autoincrement=True)

    country = Column(VARCHAR(20))

    last_update = Column(TIMESTAMP)

    @classmethod
    def create(cls, db: DbSession, data: CountryInput) -> CountryOutput:
        new_obj = cls(
            **data.dict(),
            last_update=datetime.utcnow(),
        )
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)

        return new_obj

    @classmethod
    def get_list(cls, db: DbSession, limit: int = 10, skip: int = 0, **filters) -> List[CountryOutput]:
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: DbSession, obj_id: int) -> CountryOutput:
        return db.query(cls).filter(cls.country_id == obj_id).first()

    @classmethod
    def update(cls, db: DbSession, obj_id: int, data: CountryInput) -> CountryOutput:
        db_object = cls.get_by_id(db=db, obj_id=obj_id)
        if not db_object:
            raise HTTPException(status_code=404, detail=f'{cls.__name__} not found')

        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_object, key, value)
        db_object.last_update = datetime.utcnow()
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

        return db_object
