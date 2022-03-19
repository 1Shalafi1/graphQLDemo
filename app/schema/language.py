from datetime import datetime

from app.schema.base import AbstractSchema


class LanguageBase(AbstractSchema):
    name: str

    class Config:
        orm_mode = True


class LanguageInput(LanguageBase):
    pass


class LanguageOutput(LanguageBase):
    language_id: int
    last_update: datetime
