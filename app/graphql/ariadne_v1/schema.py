import ipdb
from ariadne import gql, ObjectType, QueryType, make_executable_schema

type_defs = gql("""
  type Query {
    actor(skip: Int, limit: Int): [Actor]
  }
  
  type Mutation {
    actor_insert_one(first_name: String!, last_name: String!): Actor!
    actor_update_one(actor_id: Int!, first_name: String!, last_name: String!): Actor!
  }
  
  type Subscription {
    counter: Int!
  }



  type Film {
    film_id: ID
    language_id: Int!
    
    title: String!
    description: String!
    release_year: String!
    rental_duration: Int!
    rental_rate: Int!
    length: Int!
    replacement_cost: Float!
    rating: String!
  
  }

  type Actor {
    actor_id: ID
    first_name: String!
    last_name: String!
    films: [Film]
  }
  
  type ActorInput {
    first_name: String!
    last_name: String!
  }
""")
