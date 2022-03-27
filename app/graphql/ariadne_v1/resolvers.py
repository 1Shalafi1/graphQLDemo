import asyncio

from ariadne import QueryType, make_executable_schema, MutationType, snake_case_fallback_resolvers

from app.database import SessionLocal
from app.graphql.ariadne_v1.schema import type_defs

from app.models.actor import Actor
from app.schema.actor import ActorOutputEnriched, ActorInput

query = QueryType()
mutation = MutationType()


@query.field('actor')
def resolve_actors(_, info, skip:int=0, limit:int=10, **filters):
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


async def counter_generator(obj, info):
    for i in range(5):
        await asyncio.sleep(1)
        yield i


schema = make_executable_schema(type_defs, [query, mutation])
