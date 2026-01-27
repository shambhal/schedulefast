from fastapi import FastAPI
from fastapi import APIRouter,Depends,Path
from sqlalchemy.orm import Session
from core.database import get_db
from models.category import PMS
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import importlib


router = APIRouter()
@router.get('/list')
def allpms(db:Session=Depends(get_db)):
    results = db.query(PMS).filter(PMS.status == 1).all()
    return results  
class PaymentFormRequest(BaseModel):
    order_id: int

@router.post('/{gateway}/getform')



def get_payment_form(gateway: str,post: PaymentFormRequest):
    if(1==1):
        # Dynamically import the module
        module = importlib.import_module(f"gateways.{gateway}")
        
        # Check if getform exists
        if not hasattr(module, "getform"):
            raise HTTPException(status_code=400, detail="Invalid payment gateway")
        
        # Call getform() from the module
        return module.getform(post.order_id)
    
    #except ModuleNotFoundError:
     #   raise HTTPException(status_code=404, detail="Payment gateway not found")
@router.post('/{gateway}/process')



def process(gateway: str,data:dict):
    try:
        # Dynamically import the module
        module = importlib.import_module(f"gateways.{gateway}")
        
        # Check if getform exists
        if not hasattr(module, "getform"):
            raise HTTPException(status_code=400, detail="Invalid payment gateway")
        
        # Call getform() from the module
        return module.process(data['order_id'],data)
    
    except ModuleNotFoundError:
        raise HTTPException(status_code=404, detail="Payment gateway not found")