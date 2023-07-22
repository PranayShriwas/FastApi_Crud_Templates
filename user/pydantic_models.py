from pydantic import BaseModel


class Person(BaseModel):
    name: str
    email: str
    phone: int
    password: str


class data(BaseModel):
    id: int


class delete_data(BaseModel):
    id: int


class update(BaseModel):
    id: str
    name: str
    email: str
    phone: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Login(BaseModel):
    email: str
    password: str
