from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import ForeignKey, VARCHAR
from sqlalchemy import Integer, Column, TIMESTAMP, Index, LargeBinary, Boolean
from sqlalchemy.orm import Session as DbSession

from app.database import Base
from app.schema.customer import CustomerOutput, CustomerInput


class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = (
        Index('customer_pkey', 'customer_id'),
        Index('idx_fk_address_id', 'address_id'),
        Index('idx_fk_store_id', 'store_id'),
        Index('idx_last_name', 'last_name'),
    )

    customer_id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.address_id', name='customer_address_id_fkey'))
    store_id = Column(Integer, ForeignKey('store.store_id', name='customer_store_id_fkey'))

    first_name = Column(VARCHAR(45))
    last_name = Column(VARCHAR(45))
    email = Column(VARCHAR(50))
    active = Column(Boolean)
    create_date = Column(TIMESTAMP)
    last_update = Column(TIMESTAMP)

    @classmethod
    def create(cls, db: DbSession, data: CustomerInput) -> CustomerOutput:
        new_obj = cls(
            **data.dict(),
            last_update=datetime.utcnow(),
            create_date=datetime.utcnow(),
        )
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)

        return new_obj

    @classmethod
    def get_list(cls, db: DbSession, limit: int = 10, skip: int = 0) -> List[CustomerOutput]:
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: DbSession, customer_id: int) -> CustomerOutput:
        return db.query(cls).filter(cls.customer_id == customer_id).first()

    @classmethod
    def update(cls, db: DbSession, customer_id: int, data: CustomerInput) -> CustomerOutput:
        db_object = cls.get_by_id(db=db, customer_id=customer_id)
        if not db_object:
            raise HTTPException(status_code=404, detail='Address not found')

        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_object, key, value)
        db_object.last_update = datetime.utcnow()
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

        return db_object
