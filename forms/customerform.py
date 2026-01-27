
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re
class UserBase(BaseModel):
    name: str
    email: str
class UserLogin(BaseModel):
    email: str
    password: str
    @field_validator("password")
    def passowrd_six(cls, v):
        if  len(v)< 6:
            raise ValueError("Password should be at least 6 characters long.")
        return v  
    @field_validator("email")
    def email_format(cls,v):
        regex='^\w+\.*\w+@{1}\w+\.{1}\w+$'
        if not re.match(regex,v.strip()):
            raise ValueError("Email should have email value")
        return v
class UserCreate(UserBase):
    password: str
    phone: str   # 👈 include mobile during registration
    @field_validator("name")
    def name_required(cls, v):
        if not v.strip():
            raise ValueError("Name is required")
        return v
    @field_validator("email")
    def email_format(cls,v):
        regex='^\w+\.*\w+@{1}\w+\.{1}\w+$'
        if not re.match(regex,v.strip()):
            raise ValueError("Email should have email value")
        return v
    @field_validator("phone")
    def phone_must_be_10_digits(cls, v):
        if not v.isdigit() or len(v)<= 5:
            raise ValueError("Phone must be a 10-digit number")
        return v
    
    @field_validator("password")
    def passowrd_six(cls, v):
        if  len(v)< 6:
            raise ValueError("Password should be at least 6 characters long.")
        return v
class UserResponse(UserBase):
    id: int
    class Config:
       from_attributes = True
    @staticmethod
    def from_orm(obj):
        return UserResponse(
            id=obj.id,
            email=obj.email,
            name=f"{obj.first_name} {obj.last_name}".strip()
        )   

class CustomerResponse(BaseModel):
    id: int
    phone: str
    user: UserResponse
    class Config:
        orm_mode = True
