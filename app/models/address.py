from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import ForeignKey, VARCHAR
from sqlalchemy import Integer, Column, TIMESTAMP, Index
from sqlalchemy.orm import Session as DbSession

from app.database import Base
from app.schema.address import AddressInput, AddressOutput


class Address(Base):
    __tablename__ = 'address'
    __table_args__ = (
        Index('address_pkey', 'address_id'),
        Index('idx_fk_city_id', 'city_id'),
    )

    address_id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.city_id', name='fk_address_city'))

    address = Column(VARCHAR(50))
    address2 = Column(VARCHAR(50))
    district = Column(VARCHAR(20))
    postal_code = Column(VARCHAR(10))
    phone = Column(VARCHAR(20))
    last_update = Column(TIMESTAMP)

    @classmethod
    def create(cls, db: DbSession, data: AddressInput) -> AddressOutput:
        new_obj = cls(
            **data.dict(),
            last_update=datetime.utcnow(),
        )
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)

        return new_obj

    @classmethod
    def get_list(cls, db: DbSession, limit: int = 10, skip: int = 0) -> List[AddressOutput]:
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: DbSession, address_id: int) -> AddressOutput:
        return db.query(cls).filter(cls.address_id == address_id).first()

    @classmethod
    def update(cls, db: DbSession, address_id: int, data: AddressInput) -> AddressOutput:
        db_object = cls.get_by_id(db=db, address_id=address_id)
        if not db_object:
            raise HTTPException(status_code=404, detail='Address not found')

        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_object, key, value)
        db_object.last_update = datetime.utcnow()
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

        return db_object
