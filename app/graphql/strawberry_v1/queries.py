from typing import List

import strawberry
from strawberry.types import Info

from app.graphql.strawberry_v1.schemas import ActorType
from app.models.actor import Actor
from app.models.film import Film
from app.schema.actor import ActorOutputEnriched, ActorOutput


@strawberry.type
class Query:

    @strawberry.field
    def actors(self, info: Info, skip: int = 0, limit: int = 10) -> List[ActorType]:
        actors_objs = Actor.get_list(db=info.context['db'], limit=limit, skip=skip)
        return [ActorType.from_pydantic(ActorOutputEnriched.from_orm(x)) for x in actors_objs]


