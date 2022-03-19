from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import ForeignKey, VARCHAR
from sqlalchemy import Integer, Column, TIMESTAMP, Index, LargeBinary, Boolean
from sqlalchemy.orm import Session as DbSession

from app.database import Base
from app.schema.staff import StaffOutput, StaffInput, StaffCreate


class Staff(Base):
    __tablename__ = 'staff'
    __table_args__ = (
        Index('staff_pkey', 'staff_id'),
    )

    staff_id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.address_id', name='staff_address_id_fkey'))
    store_id = Column(Integer)

    first_name = Column(VARCHAR(45))
    last_name = Column(VARCHAR(45))
    username = Column(VARCHAR(16))
    password = Column(VARCHAR(45))
    active = Column(Boolean)
    picture = Column(LargeBinary)
    last_update = Column(TIMESTAMP)

    @classmethod
    def create(cls, db: DbSession, data: StaffCreate) -> StaffOutput:
        new_obj = cls(
            **data.dict(),
            last_update=datetime.utcnow(),
        )
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)

        return new_obj

    @classmethod
    def get_list(cls, db: DbSession, limit: int = 10, skip: int = 0) -> List[StaffOutput]:
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: DbSession, staff_id: int) -> StaffOutput:
        return db.query(cls).filter(cls.staff_id == staff_id).first()

    @classmethod
    def update(cls, db: DbSession, staff_id: int, data: StaffInput) -> StaffOutput:
        db_object = cls.get_by_id(db=db, staff_id=staff_id)
        if not db_object:
            raise HTTPException(status_code=404, detail='Address not found')

        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_object, key, value)
        db_object.last_update = datetime.utcnow()
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

        return db_object
