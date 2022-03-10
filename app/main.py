import datetime

from fastapi import FastAPI
from app.routes.actor import actor_router

app = FastAPI()
app.include_router(actor_router)

@app.get('/')
def ping():
    return f'pong {datetime.datetime.utcnow()}'