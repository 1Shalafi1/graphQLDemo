import datetime

from fastapi import FastAPI
from app.routes.actor import actor_router
from app.routes.address import address_router
from app.routes.city import city_router
from app.routes.country import country_router
from app.routes.customer import customer_router
from app.routes.language import language_router
from app.routes.payment import payment_router
from app.routes.staff import staff_router
from app.routes.store import store_router
from app.routes.film import film_router


app = FastAPI()
# Routes
app.include_router(actor_router, prefix='actor')
app.include_router(address_router, prefix='address')
app.include_router(city_router, prefix='city')
app.include_router(country_router, prefix='country')
app.include_router(staff_router, prefix='staff')
app.include_router(store_router, prefix='store')
app.include_router(customer_router, prefix='customer')
app.include_router(film_router, prefix='film')
app.include_router(language_router, prefix='language')
app.include_router(payment_router, prefix='payment')

# Default endpoints
@app.get('/')
def ping():
    return f'pong {datetime.datetime.utcnow()}'
