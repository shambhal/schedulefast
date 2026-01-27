from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

import re
class GuestForm(BaseModel):
    name: str
    email: str
    phone: str

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


class OrderUpdateForm(BaseModel):
    order_id: int
    user_id :Optional[int]=0
    appointee:Optional[GuestForm]
    payment_method:str=''

    

class OrderStatusRequest(BaseModel):
    order_id: int
    email: str