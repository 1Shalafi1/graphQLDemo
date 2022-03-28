import datetime

from ariadne import QueryType, make_executable_schema, MutationType, ScalarType, EnumType

from app.database import SessionLocal
from app.graphql.ariadne_v1.schema import type_defs
from app.models.actor import Actor
from app.models.category import Category
from app.models.film import Film
from app.schema.actor import ActorOutputEnriched, ActorInput
from app.schema.category import CategoryInput
from app.schema.film import FilmInput, MPPARatingEnum

query = QueryType()
mutation = MutationType()


@query.field('actor')
def resolve_actors(_, info, skip: int = 0, limit: int = 10, **filters):
    db = SessionLocal()
    db_actors = Actor.get_list(db=db, skip=skip, limit=limit)
    results = [ActorOutputEnriched.from_orm(actor) for actor in db_actors]
    db.close()
    return results


@mutation.field('actor_insert_one')
def resolve_actor_insert_one(_, info, first_name: str, last_name: str):
    db = SessionLocal()
    obj = Actor.create(db=db, data=ActorInput(first_name=first_name, last_name=last_name))
    db.close()
    return obj


@mutation.field('actor_update_one')
def resole_actor_update_one(_, info, actor_id: int, first_name: str, last_name: str):
    db = SessionLocal()
    obj = Actor.update(db, actor_id=actor_id, data=ActorInput(first_name=first_name, last_name=last_name))
    db.close()
    return obj


@mutation.field('category_insert_one')
def resolve_category_insert_one(_, info, name: str):
    db = SessionLocal()
    obj = Category.create(db=db, data=CategoryInput(name=name))
    db.close()
    return obj



@mutation.field('film_insert_one')
def resolve_film_insert_one(_, info, input: FilmInput):
    db = SessionLocal()
    obj = Film.create(db=db, data=FilmInput(**input))
    db.close()
    return obj


datetime_scalar = ScalarType('Datetime')


@datetime_scalar.serializer
def serialize_datetime(value: datetime.datetime):
    return value.isoformat()


mppa_rating_enum = EnumType('MPPARating', MPPARatingEnum)




schema = make_executable_schema(type_defs, [query, mutation, datetime_scalar, mppa_rating_enum])
