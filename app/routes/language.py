from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db
from app.models.language import Language
from app.schema.language import LanguageBase, LanguageInput

language_router = APIRouter()


@language_router.get("/", tags=['languages'], response_model=List[LanguageBase])
def _list(skip: int = 0, limit: int = 10, db: DbSession = Depends(get_db)):
    return Language.get_list(db=db, skip=skip, limit=limit)


@language_router.get('/{language_id}', tags=['languages'], response_model=LanguageBase)
def retrieve(language_id: int, db: DbSession = Depends(get_db)):
    return Language.get_by_id(db=db, language_id=language_id)


@language_router.post('/', tags=['languages'], response_model=LanguageBase)
def create(language: LanguageInput, db: DbSession = Depends(get_db)):
    return Language.create(data=language, db=db)


@language_router.put('/{language_id}', tags=['languages'], response_model=LanguageBase)
def update(language_id: int, language: LanguageInput, db: DbSession = Depends(get_db)):
    return Language.update(data=language, language_id=language_id, db=db)
