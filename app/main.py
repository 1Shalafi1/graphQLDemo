import datetime

from fastapi import FastAPI
from app.routes.actor import actor_router
from app.routes.address import address_router
from app.routes.city import city_router
from app.routes.country import country_router
from app.routes.customer import customer_router
from app.routes.staff import staff_router
from app.routes.store import store_router


app = FastAPI()
# Routes
app.include_router(actor_router)
app.include_router(address_router)
app.include_router(city_router)
app.include_router(country_router)
app.include_router(staff_router)
app.include_router(store_router)
app.include_router(customer_router)

# Default endpoints
@app.get('/')
def ping():
    return f'pong {datetime.datetime.utcnow()}'
