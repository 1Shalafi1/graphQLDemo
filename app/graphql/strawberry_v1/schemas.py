from enum import Enum
from typing import List

import strawberry

from app.schema.actor import ActorOutput, ActorOutputEnriched, ActorInput
from app.schema.category import CategoryOutput
from app.schema.film import FilmOutput, FilmOutputWithCategories, MPPARatingEnum, FilmInput


class MPPARatingEnumType(Enum):
    G = 'G'
    PG = 'PG'
    PG13 = 'PG-13'
    R = 'R'
    NC17 = 'NC-17'

strawberry.enum(MPPARatingEnum)


@strawberry.experimental.pydantic.type(model=CategoryOutput, all_fields=True)
class CategoriesType:
    pass


@strawberry.experimental.pydantic.type(model=FilmOutputWithCategories, all_fields=True)
class FilmType:
    pass


@strawberry.experimental.pydantic.type(model=ActorOutputEnriched)
class ActorType:
    actor_id: strawberry.auto
    films: strawberry.auto
    first_name: strawberry.auto
    last_name: strawberry.auto
    last_update: strawberry.auto


@strawberry.experimental.pydantic.input(model=ActorInput, all_fields=True)
class ActorInputType:
    pass


@strawberry.experimental.pydantic.input(model=FilmInput, all_fields=True)
class FilmInputType:
    pass