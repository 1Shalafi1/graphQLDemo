from fastapi import Depends
from sqlalchemy.orm import Session as DbSession

from app.dependencies import get_db


async def get_context(db: DbSession = Depends(get_db)):
    return {
        "db": db,
    }