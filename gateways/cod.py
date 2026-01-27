from fastapi import APIRouter,Depends,Path
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import  SERVER_OFFSET,BOOKING_GAP
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey,UniqueConstraint,Date,Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from core.database import get_db
from models.category import Order
from core.database import SessionLocal  # use SessionLocal instead of get_db
Base = declarative_base()
class COD(Base):

      __tablename__ = "cod_cod"
      status = Column(Integer, primary_key=True, index=True)
def process(order_id:int,data:dict):
    #print(data)
    email=data['appointee']['email'] 
    with SessionLocal() as db:
       q= db.query(Order).filter(Order.id==order_id).filter(Order.email==email).first()
       if q  and q.status=='CREATED':
           q.status='PROCESSING'
           db.commit()

           return {'success':1}
            
    
def getform(order_id: int):
    # Ideally use a session context manager
    with SessionLocal() as db:
        f = db.query(COD).filter(COD.status == 1).first()
        if f is None:
            return {"form": None}

        action = "payments/cod/process"
        return {
             "actionurl":action,
            "form": f"""
               
                    <input type="hidden" name="order_id" value="{order_id}"/>
                    <button type="submit">Confirm</button>
                
            """
        }
