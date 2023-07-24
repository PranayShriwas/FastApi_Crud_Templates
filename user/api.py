import passlib
import typing
from json import JSONEncoder
from fastapi.encoders import jsonable_encoder
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from passlib.context import CryptContext
from . pydantic_models import Token
from fastapi import APIRouter, Request, status, Depends, Form
from .models import *
from . pydantic_models import Person, data, delete_data, update, Login
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

app = APIRouter()
# SECRET = 'your-secret-key'

# manager = LoginManager(SECRET, token_url='/user_login')
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# manager = LoginManager(SECRET, token_url='/login')


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


@app.post('/')
async def registration(data: Person):
    if await Student.exists(phone=data.phone):
        return {"status": False, "message": "Phone number already exists"}
    elif await Student.exists(email=data.email):
        return {"status": False, "message": "Email already exits"}
    else:
        user_obj = await Student.create(name=data.name, email=data.email, phone=data.phone, password=get_password_hash(data.password))
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


# @manager.user_loader()
# async def load_user(email: str):
#     if await Student.exists(email=email):
#         user = await Student.get(email=email)
#         return user


# @app.post('/login/')
# async def login(data: Login):
#     email = data.email
#     user = await load_user(email)

#     if not user:
#         return JSONResponse({'status': False, 'message': 'User not Registered'}, status_code=403)
#     elif not verify_password(data.password, user.password):
#         return JSONResponse({'status': False, 'message': 'Invalid password'}, status_code=403)
#     access_token = manager.create_access_token(data={'sub': {'id': user.id}})
#     new_dict = jsonable_encoder(user)
#     new_dict.update({'access_token': access_token})
#     return Token(access_token=access_token, token_type='bearer')
