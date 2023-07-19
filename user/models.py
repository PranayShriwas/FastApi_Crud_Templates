from tortoise.models import Model
from tortoise import Tortoise, fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    email = fields.CharField(50, unique=True)
    phone = fields.CharField(10)
    password = fields.CharField(250)


Tortoise.init_models(['user.models'], "models")
