from datetime import datetime
from typing import List

import fastapi.exceptions
from fastapi import HTTPException
from sqlalchemy import ForeignKey, VARCHAR, Text, Numeric, String, ARRAY
from sqlalchemy import Integer, Column, TIMESTAMP, Index, LargeBinary, Boolean
from sqlalchemy.orm import Session as DbSession

from app.database import Base
from app.schema.film import FilmOutput, FilmInput


class Payment(Base):
    __tablename__ = 'payment'
    __table_args__ = (
        Index('payment_pkey', 'payment_id'),
        Index('idx_fk_customer_id', 'customer_id'),
        Index('idx_fk_rental_id', 'rental_id'),
        Index('idx_fk_staff_id', 'staff_id'),
    )

    payment_id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id', name='payment_staff_id_fkey'))
    rental_id = Column(Integer, ForeignKey('rental.rental_id', name='payment_rental_id_fkey'))
    customer_id = Column(Integer, ForeignKey('customer.customer_id', name='payment_customer_id_fkey'))
    amount = Column(Numeric)

    payment_date = Column(TIMESTAMP)

    @classmethod
    def create(cls, db: DbSession, data: FilmInput) -> FilmOutput:
        new_obj = cls(
            **data.dict(),
            payment=datetime.utcnow(),
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
        raise HTTPException(status_code=405, detail='Method update is not allowed')
