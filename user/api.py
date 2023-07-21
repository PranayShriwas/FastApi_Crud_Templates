from fastapi.encoders import jsonable_encoder
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from . pydantic_models import Person, data, delete_data, update
from .pydantic_models import Token
from fastapi import APIRouter, Request, status, Depends
from .models import *


app = APIRouter()


@app.post('/')
async def registration(data: Person):
    if await Student.exists(mobile=data.phone):
        return {"status": False, "message": "Phone number already exists"}
    elif await Student.exists(email=data.email):
        return {"status": False, "message": "Email already exits"}
    else:
        user_obj = await Student.create(name=data.name, email=data.email, mobile=data.phone, password=get_password_hash(data.password))
        return user_obj


@app.get('/all/')
async def all_student():
    user_obj = await Student.all()
    return user_obj


@app.post('/Search_by_id/')
async def data(data: data):
    user_object = await Student.filter(id=data.id)
    return user_object


@app.delete('/delete_Student/')
async def delete_Student(data: delete_data):
    user_obj = await Student.filter(id=data.id).delete()
    return user_obj


@app.put('/update_stu/')
async def update_student(data: update):
    student_obj = await Student.get(id=data.id)
    if not student_obj:
        return {"status": False, "message": "Student is not exists"}
    else:
        student_obj = await Student.filter(id=data.id).update(name=data.name, email=data.email, phone=data.phone)
        return student_obj
