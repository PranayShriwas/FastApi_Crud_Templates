from fastapi import APIRouter, Request, Form, status
from fastapi.templating import Jinja2Templates
from . models import *
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.context import CryptContext
import typing

router = APIRouter()

templates = Jinja2Templates(directory="user/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append(
        {"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.get('/', response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse('index.html', {
        "request": request
    })


@router.post("/registration/", response_class=HTMLResponse)
async def ragistration(request: Request, name: str = Form(...),
                       email: str = Form(...),
                       phone: str = Form(...),
                       password: str = Form(...)):
    if await Student.filter(email=email).exists():
        flash(request, "Email already Exists")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    elif await Student.filter(phone=phone).exists():
        flash(request, "Phone Number already Exists")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    else:
        await Student.create(name=name, email=email, phone=phone, password=get_password_hash(password))
        flash(request, "Student sucessfull Ragistrated")
        return RedirectResponse("/table/", status_code=status.HTTP_201_CREATED)


@router.get('/table/', response_class=HTMLResponse)
async def read_userm(request: Request):
    user = await Student.all()
    return templates.TemplateResponse('table.html', {
        "user": user,
        "request": request
    })


@router.get("/login/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
    })


@router.post('/loginuser/')
async def login(request: Request, Phone: str = Form(...),
                Password: str = Form(...)):
    Phone = Phone
    user = await load_user(Phone)
    if not user:
        return {'USER NOT REGISTERED'}
    elif not verify_password(Password, user.password):
        return {'PASSWORD IS WRONG'}
    access_token = manager.create_access_token(
        data=dict(sub=Phone)
    )
    if "_messages" not in request.session:
        request.session['_messages'] = []
        new_dict = {"user_id": str(
            user.id), "Phone": Phone, "access_token": str(access_token)}
        request.session['_messages'].append(
            new_dict
        )
    return RedirectResponse('/welcome/', status_code=status.HTTP_302_FOUND)


@router.get("/update/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):
    user = await Student.get(id=id)
    return templates.TemplateResponse("update.html", {
        "request": request,
        "user": user
    })


@router.post("/update_detials/")
async def update(request: Request, id: int = Form(...),
                 name: str = Form(...),
                 email: str = Form(...),
                 phone: str = Form(...),
                 ):
    user = await Student.get(id=id)
    await user.filter(id=id).update(name=name,
                                    email=email, phone=phone
                                    )
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)


@router.get("/delete/{id}", response_class=HTMLResponse)
async def delete(request: Request, id: int):
    user = await Student.get(id=id).delete()
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)
