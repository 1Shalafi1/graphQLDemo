from datetime import datetime

from pydantic import BaseModel


class ActorBase(BaseModel):
    actor_id: int
    first_name: str
    last_name: str
    last_update: datetime

    class Config:
        orm_mode = True

class ActorInput(BaseModel):
    first_name: str
    last_name: str
