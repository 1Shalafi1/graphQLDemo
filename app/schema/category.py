from datetime import datetime

from app.schema.base import AbstractSchema


class CategoryBase(AbstractSchema):
    name: str

    class Config:
        orm_mode = True


class CategoryInput(CategoryBase):
    pass


class CategoryOutput(CategoryBase):
    category_id: int
    last_update: datetime
