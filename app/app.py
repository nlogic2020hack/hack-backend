from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from nlogic.fastapi.app import register_routers

from settings.config import settings
from .routers.v1.app import compiled_routers

app = register_routers(
    routers=[compiled_routers],
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(app=app, config=settings.db_conn(), generate_schemas=True)
