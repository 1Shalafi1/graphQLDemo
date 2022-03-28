from typing import List

from graphene import ObjectType, String, Schema, Int, DateTime, Decimal


class Films(ObjectType):
    film_id = Int()
    language_id: Int()

    title: String()
    description: String()
    release_year: String()
    rental_duration: Int()
    rental_rate: Int()
    length: Int()
    replacement_cost: Decimal()
    rating: String()

    special_features: List[String()]

    fulltext: String()

class Actor(ObjectType):
    actor_id = Int()

    first_name = String()
    last_name = String()
    last_update= String()

    def resolve_full_name(parent, info):
        return f"{parent.first_name} {parent.last_name}"



class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    actor = ""
    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_actor(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'