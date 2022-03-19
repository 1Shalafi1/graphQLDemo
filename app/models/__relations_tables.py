from sqlalchemy import Table, Column, Integer, ForeignKey

from app.database import Base

film_actor = Table(
    'film_actor',
    Base.metadata,
    Column('actor_id', Integer, ForeignKey('actor.actor_id')),
    Column('film_id', Integer, ForeignKey('film.film_id')),
)

film_category = Table(
    'film_category',
    Base.metadata,
    Column('category_id', Integer, ForeignKey('category.category_id')),
    Column('film_id', Integer, ForeignKey('film.film_id')),
)
