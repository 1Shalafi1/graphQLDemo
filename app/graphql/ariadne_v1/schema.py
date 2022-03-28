import ipdb
from ariadne import gql, ObjectType, QueryType, make_executable_schema

type_defs = gql("""
  enum MPPARating {
    G
    PG
    PG13
    R
    NC17
  }

  type Query {
    actor(skip: Int, limit: Int): [Actor]
  }
  
  type Mutation {
    actor_insert_one(first_name: String!, last_name: String!): Actor!
    actor_update_one(actor_id: Int!, first_name: String!, last_name: String!): Actor!
    
    category_insert_one(name: String!): Category!
    
    film_insert_one(input: FilmInput): Film!    
  }
  
  scalar Datetime
  
  type Category {
    name: String!
    category_id: Int!
    last_update: Datetime
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
    rating: MPPARating!
    last_update: Datetime
    categories: [Category]
  }

  input FilmInput {
    language_id: Int!
    title: String!
    description: String!
    release_year: String!
    rental_duration: Int!
    rental_rate: Int!
    length: Int!
    replacement_cost: Float!
    rating: MPPARating!   
  }

  type Actor {
    actor_id: ID
    first_name: String!
    last_name: String!
    last_update: Datetime
    films: [Film]
  }
  
  type ActorInput {
    first_name: String!
    last_name: String!
  }
  
  fragment testField on Film {
    film_id
    title
    description
    categories {
        category_id
        name
        }
    }  

""")
