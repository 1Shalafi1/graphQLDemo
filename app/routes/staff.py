from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.staff import Staff
from app.schema.staff import StaffOutput, StaffInput, StaffCreate

staff_router = APIRouter()


@staff_router.get("/", tags=['Staff'], response_model=List[StaffOutput])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Staff.get_list(db=db, skip=skip, limit=limit)


@staff_router.get('/{staff_id}', tags=['Staff'], response_model=StaffOutput)
def retrieve(staff_id: int, db: DbSession = Depends(get_db)):
    return Staff.get_by_id(db=db, staff_id=staff_id)


@staff_router.post('/', tags=['Staff'], response_model=StaffOutput)
def create(staff: StaffCreate, db: DbSession = Depends(get_db)):
    return Staff.create(data=staff, db=db)


@staff_router.put('/{staff_id}', tags=['Staff'], response_model=StaffOutput)
def update(staff_id: int, staff: StaffInput, db: DbSession = Depends(get_db)):
    return Staff.update(data=staff, staff_id=staff_id, db=db)
