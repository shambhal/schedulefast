from pydantic import BaseModel,Field,EmailStr
from fastapi import Form


class ContactForm(BaseModel):
    name: str = Field(..., min_length=4)
    email: str
    query: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(..., min_length=4),
         email:str=Form('Email',min_length=10,regex="^\w+\.*\w+@{1}\w+\.{1}\w+$"),
        query: str = Form(...),
    ) -> "ContactForm":
        return cls(name=name, email=email, query=query)
