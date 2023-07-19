from fastapi import APIRouter, Request, Form, status
from .models import User
from .pydantic_models import Person

app = APIRouter()


@app.post('/registration_api/')
async def registration(data: Person):
    if await User.exists(phone=data.phone):
        return {'status': False, 'message': 'Phone Number Already Exists'}
    elif await User.exists(email=data.email):
        return {'status': False, 'message': 'Phone Number Already Exists'}
    else:
        user_obj = await User.create(name=data.name, email=data.email, phone=data.phone, password=data.password)
        return user_obj
