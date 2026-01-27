from fastapi import APIRouter,Depends,Path
from sqlalchemy.orm import Session
from core.database import get_db
from .utils import getSlotPrice
from forms.cartform import CartCreate,FetchCart,CartDelItem
from models.category import Cart,Doctor
from datetime import datetime as dt
from datetime import timedelta
from typing import Optional
router = APIRouter()

@router.post('/add')
def add_cart(fc:CartCreate, db: Session = Depends(get_db)):
    mm=fc.model_dump()
   
    mm['price']=getSlotPrice(mm['doctor_id'],mm['slot'],mm['dated'],db)
    #cd=dt.now()-timedelta(days=1)
    docinfo=db.query(Doctor).filter(Doctor.id==mm['doctor_id']).first()
    mm['doctor_name']=docinfo.first_name + ' '+docinfo.last_name if docinfo else ''
    print(docinfo)
    '''
    db.query(Cart).filter(mm['uuid']==Cart.device_id).filter(Cart.dated<=cd.date()).delete()
    ##delete old same slot 
    db.query(Cart).filter(mm['uuid']==Cart.device_id).filter(Cart.dated==mm['dated']).filter(Cart.doctor_id==mm['doctor_id']).filter(Cart.slot==mm['slot']).delete()
    d= db.query(Cart).filter(mm['uuid']==Cart.device_id).order_by(Cart.dated).all()
    '''
    delete_old({'uuid':mm['device_id']})
    if(1==1):
      rec=Cart(**mm)
      db.query(Cart).filter(mm['device_id']==Cart.device_id).filter(Cart.doctor_id==mm['doctor_id']).filter(Cart.dated==mm['dated']).filter(Cart.slot==mm['slot']).delete()
      db.add(rec)
      db.commit()
      db.refresh(rec)
      return {'success':1,'record':rec}
    #except  Exception as e:
    else:
     e='h'
     return {'error':1 ,'message':e} 
    #finally:
      #  return {'success':1} 
   
@router.post('/getcart')
def fetch_cart(fc:FetchCart,db:Session=Depends(get_db)):
     mm=fc.model_dump()
     delete_old(mm)
     d= db.query(Cart).filter(Cart.device_id==mm['uuid']).order_by(Cart.dated).all()
     def getSubtotal(d):
        total=0
        for item in d:
           total=total+float(item.price)
           #print(item.price)
        return total
     return {'items':d,'subtotal':getSubtotal(d)}
    
def delete_old(mm): 
   db = next(get_db())
   cd=dt.now()-timedelta(days=1)
   db.query(Cart).filter(Cart.device_id==mm['uuid']).filter(Cart.dated<=cd.date()).delete()
#@router.get('/cart')
   db.commit()
#
@router.post('/clear')
def clearcart(post:dict,db:Session=Depends(get_db)):
   uuid = post.get('uuid', '')
   db.query(Cart).filter(Cart.device_id==uuid).delete()
   d= db.query(Cart).filter(Cart.device_id==uuid).order_by(Cart.dated).all()
   def getSubtotal(d):
        total=0
        for item in d:
           total=total+float(item.price)
           #print(item.price)
        return total
   return {'items':d,'subtotal':getSubtotal(d)}
@router.post('/delete')
def deleteitem(item:CartDelItem,db:Session=Depends(get_db)):
  
 
   db.query(Cart).filter(Cart.device_id==item.uuid).filter(Cart.id==item.id).delete()
   db.commit()
   d= db.query(Cart).filter(Cart.device_id==item.uuid).order_by(Cart.dated).all()
   def getSubtotal(d):
        total=0
        for item in d:
           total=total+float(item.price)
           #print(item.price)
        return total
   return {'items':d,'subtotal':getSubtotal(d)}

