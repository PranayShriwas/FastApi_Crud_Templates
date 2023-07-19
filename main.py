from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI()
register_tortoise(
    app,
    db_url="postgres://postgres:root@127.0.0.1/crud",
    modules={'models': ['user.models']},
    generate_schemas=True,
    add_exception_handlers=True
)
