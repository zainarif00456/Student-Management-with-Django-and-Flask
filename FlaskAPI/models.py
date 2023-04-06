from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    _id: int
    name: str
    fathers_name: str
    fathers_cnic: str
    fathers_phone: str
    gender: str
    date_of_birth: str
    class_enrolled: str


class Admin(BaseModel):
    full_name: str
    cnic: str
    gender: str
    date_of_birth: str
    email_address: str
    user_name: str
    password: str


class AdminLogin(BaseModel):
    user_name: str
    password: str
