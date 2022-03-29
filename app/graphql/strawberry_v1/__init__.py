import strawberry

from app.graphql.strawberry_v1.mutations import Mutation
from app.graphql.strawberry_v1.queries import Query

schema = strawberry.Schema(Query, Mutation)