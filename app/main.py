import datetime

from fastapi import FastAPI
from app.routes.actor import actor_router
from app.routes.address import address_router
from app.routes.city import city_router
from app.routes.country import country_router

app = FastAPI()
app.include_router(actor_router)
app.include_router(address_router)
app.include_router(city_router)
app.include_router(country_router)


@app.get('/')
def ping():
    return f'pong {datetime.datetime.utcnow()}'
