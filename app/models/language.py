from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import Integer, Column, TIMESTAMP, Index, LargeBinary, Boolean, Text
from sqlalchemy.orm import Session as DbSession

from app.database import Base
from app.schema.language import LanguageOutput, LanguageInput


class Language(Base):
    __tablename__ = 'language'
    __table_args__ = (
        Index('language_pkey', 'language_id'),
    )

    language_id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    name = Column(Text)
    last_update = Column(TIMESTAMP)

    @classmethod
    def create(cls, db: DbSession, data: LanguageInput) -> LanguageOutput:
        new_obj = cls(
            **data.dict(),
            last_update=datetime.utcnow(),
        )
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)

        return new_obj

    @classmethod
    def get_list(cls, db: DbSession, limit: int = 10, skip: int = 0) -> List[LanguageOutput]:
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: DbSession, language_id: int) -> LanguageOutput:
        return db.query(cls).filter(cls.language_id == language_id).first()

    @classmethod
    def update(cls, db: DbSession, language_id: int, data: LanguageInput) -> LanguageOutput:
        db_object = cls.get_by_id(db=db, language_id=language_id)
        if not db_object:
            raise HTTPException(status_code=404, detail='Address not found')

        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_object, key, value)
        db_object.last_update = datetime.utcnow()
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

        return db_object
