from fastapi import APIRouter,Depends,Path
from sqlalchemy.orm import Session
from core.database import get_db
from typing import Optional
from models.category import Category,Doctor,DoctorCategory,DoctorQ
#from fastapi_pagination.ext.sqlalchemy import paginate
#from fastapi_pagination import Page, add_pagination, paginate
router = APIRouter()
@router.get('/')
async def getcats(db:Session=Depends(get_db)):
    q = db.query(Category)
    q = q.filter(Category.is_active == True)
    q=q.filter(
        Category.parent_id.is_(None)
    )
    q = q.order_by(Category.name)  # use the actual column, not a string
    return {'categories':q.all()}
    #return q.all()
   
from enum import Enum
'''
class Ramparams(str,Enum):
    saviour='Ram'
    victim='Sita'
    villain='Ravan'
@router.get('/{ramayan}')
def ramp(ramayan:Ramparams): 

    if(ramayan is Ramparams.saviour): 
     return {"you selected ram"} 
    elif (ramayan is Ramparams.victim) :
     return {"you selected ram"} 
    else :
     return {"upi se;ec;ected raavan"} 

    return {"model_name": ramayan, "message": "Have some residuals"}  

    doctors = (
    db.query(Doctor)
    .join(DoctorCategory, Doctor.id == DoctorCategory.doctor_id)
    .filter(DoctorCategory.category_id == id)
    .all()
)


'''    
@router.get("/basic/{slug}/{id}")
def basicinfo(slug:str,id:Optional[int]=None,db:Session=Depends(get_db)):
    if id!=None:
        d=db.query(Category).filter(Category.id==id).first()
       
        return {'info':d}
    
    d=db.query(Category).filter(Category.slug==slug).all()
  
    return {'info':d}
    

@router.get("/{slug}") 
@router.get("/{slug}/{id}")
def catinfo(slug:str,id:Optional[int]=None,db:Session=Depends(get_db)):
    if id!=None:
        d=db.query(Category).filter(Category.id==id).all()
        subcat=db.query(Category).filter(Category.parent_id==id).all()
        doctors=db.query(Doctor).join(Doctor.categories).filter(Category.id==id).all()
        return {'info':d,'subcats':subcat,'doctors':doctors}
    
    d=db.query(Category).filter(Category.slug==slug).all()
    subcat=db.query(Category).filter(Category.parent==id).all()
    doctors=db.query(Doctor).join(DoctorCategory ,DoctorCategory.doctor_id==Doctor.id).filter(DoctorCategory.id==id).all()
    return {'info':d,'subcat':subcat}
    
    
