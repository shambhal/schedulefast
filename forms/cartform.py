# schemas/cart.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

class CartBase(BaseModel):
    dated: str
    #price: condecimal(max_digits=6, decimal_places=2)
    slot: str
    device_id: Optional[str] = None
    user_id: Optional[int] = None
    doctor_id: int
    category_id:Optional[int]=0
    category_name:Optional[str]=None

class CartCreate(CartBase):
    pass
class CartDelete(CartBase):
    pass
class CartDelItem(BaseModel):
    id:int
    uuid:str
class CartRead(CartBase):
    id: int

    class Config:
       from_attributes = True
class FetchCart(BaseModel):
    uuid:str='f6fd7f-898e-497c-b348-6c69b4b4'