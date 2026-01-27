from fastapi import APIRouter,Depends,Path,Request,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from core.config import  SERVER_OFFSET,BOOKING_GAP
from typing import Optional
from  datetime import datetime,timedelta
from forms.guestform import GuestForm,OrderUpdateForm,OrderStatusRequest
from models.category import Order,Category,Doctor,User
from .utils import getSlotPrice
from .user import verify_token
router = APIRouter()
@router.get("/me")
def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalid or expired")

    user_email = payload.get("sub")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/orders/", response_model=Page[Order])
def list_my_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = (
        db.query(Order)
        .filter(Order.email == user.email)
        .order_by(Order.created_at.desc())
    )
    return sqlalchemy_paginate(db, query)