from fastapi import APIRouter,Depends,Path
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import  SERVER_OFFSET,BOOKING_GAP
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey,UniqueConstraint,Date,Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from core.database import get_db
Base = declarative_base()
class Paypal(Base):

       __tablename__ = "paypal_paypal"
       email = Column(String(100), unique=True, index=True)
       status = Column(Integer, nullable=True)
       sandbox = Column(Integer, nullable=True)
       transaction = Column(String(40), nullable=True)
def post_form(ord:dict):
   db=get_db()

   r=db.query(Paypal).first()
   return f"""
    <form method="POST" action="/api/order/confirm?order_id={order_id}">
      <button type="submit">Confirm Cash on Delivery</button>
    </form>
    """