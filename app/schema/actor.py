from datetime import datetime

from app.schema.base import AbstractSchema


class ActorBase(AbstractSchema):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class ActorInput(ActorBase):
    pass


class ActorOutput(ActorBase):
    actor_id: int
    last_update: datetime
