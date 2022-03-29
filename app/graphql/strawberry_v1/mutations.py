import strawberry
from strawberry.types import Info

from app.graphql.strawberry_v1.schemas import ActorInputType, ActorType, FilmInputType, FilmType
from app.models.actor import Actor
from app.models.film import Film
from app.schema.actor import ActorInput, ActorOutput


@strawberry.type
class Mutation:

    @strawberry.field
    def actor_insert_one(self, info: Info, actor_input: ActorInputType) -> ActorType:
        actor_obj = Actor.create(db=info.context['db'], data=actor_input.to_pydantic())
        return ActorType.from_pydantic(actor_obj)


    @strawberry.field
    def actor_update_one(self, info: Info, actor_id: int, actor_input: ActorInputType) -> ActorType:
        actor_obj = Actor.update(db=info.context['db'], actor_id=actor_id, data=actor_input.to_pydantic())
        return ActorType.from_pydantic(actor_obj)


    @strawberry.field
    def film_insert_one(self, info: Info, film_input: FilmInputType) -> FilmType:
        film_obj = Film.create(db=info.context['db'], data=film_input.to_pydantic())
        return FilmType.from_pydantic(film_obj)


    @strawberry.field
    def category_insert_one(self, info: Info, film_input: FilmInputType) -> FilmType:
        film_obj = Film.create(db=info.context['db'], data=film_input.to_pydantic())
        return FilmType.from_pydantic(film_obj)