from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import ForeignKey, VARCHAR
from sqlalchemy import Integer, Column, TIMESTAMP, Index
from sqlalchemy.orm import Session as DbSession

from app.database import Base
from app.schema.store import StoreOutput, StoreInput


class Store(Base):
    __tablename__ = 'store'
    __table_args__ = (
        Index('store_pkey', 'store_id'),
        Index('idx_unq_manager_staff_id', 'manager_staff_id'),
    )

    store_id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.address_id', name='store_address_id_fkey'))
    manager_staff_id = Column(Integer, ForeignKey('staff.staff_id', name='store_manager_staff_id_fkey'))

    last_update = Column(TIMESTAMP)

    @classmethod
    def create(cls, db: DbSession, data: StoreInput) -> StoreOutput:
        new_obj = cls(
            **data.dict(),
            last_update=datetime.utcnow(),
        )
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)

        return new_obj

    @classmethod
    def get_list(cls, db: DbSession, limit: int = 10, skip: int = 0) -> List[StoreOutput]:
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: DbSession, obj_id: int) -> StoreOutput:
        return db.query(cls).filter(cls.store_id == obj_id).first()

    @classmethod
    def update(cls, db: DbSession, obj_id: int, data: StoreInput) -> StoreOutput:
        db_object = cls.get_by_id(db=db, obj_id=obj_id)
        if not db_object:
            raise HTTPException(status_code=404, detail='Address not found')

        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_object, key, value)
        db_object.last_update = datetime.utcnow()
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

        return db_object
