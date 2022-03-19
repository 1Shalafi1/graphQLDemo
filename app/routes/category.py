from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.category import Category
from app.schema.category import CategoryInput, CategoryOutput

category_router = APIRouter()


@category_router.get("/", tags=['Categories'], response_model=List[CategoryOutput])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Category.get_list(db=db, skip=skip, limit=limit)


@category_router.get('/{category_id}', tags=['Categories'], response_model=CategoryOutput)
def retrieve(category_id: int, db: DbSession = Depends(get_db)):
    return Category.get_by_id(db=db, obj_id=category_id)


@category_router.post('/', tags=['Categories'], response_model=CategoryOutput)
def create(category: CategoryInput, db: DbSession = Depends(get_db)):
    return Category.create(data=category, db=db)


@category_router.put('/{category_id}', tags=['Categories'], response_model=CategoryOutput)
def update(category_id: int, category: CategoryInput, db: DbSession = Depends(get_db)):
    return Category.update(data=category, obj_id=category_id, db=db)
