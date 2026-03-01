from fastapi import APIRouter,Depends,Path
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import  SERVER_OFFSET,BOOKING_GAP
from typing import Optional
from  datetime import datetime,timedelta
from core.time import SERVER_TZ
from models.category import Doctor,DoctorSpecial,Book,DoctorQ,Config
#from fastapi_pagination.ext.sqlalchemy import paginate
#from fastapi_pagination import Page, add_pagination, paginate
router = APIRouter()


@router.get('/')
async def index(db:Session=Depends(get_db)):
    q = db.query(Doctor)
    q = q.filter(Doctor.is_active == True)
    
    q = q.order_by(Doctor.name)  # use the actual column, not a string
    return {'categories':q.all()}
    #return q.all()
@router.get('/maintenance')
async def index(db:Session=Depends(get_db)):
   value = (
        db.query(Config.value)
        .filter(Config.cname == "mmd")
        .scalar()
    )
   return {"maintenance": value == "1"}
    
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
@router.get("/basic/{id}")
def basicinfo(id:Optional[int]=None,db:Session=Depends(get_db)):
    if id!=None:
        d=db.query(Doctor).filter(Doctor.id==id).first()
       
        return {'info':d}
from datetime import datetime, timedelta
import json

def get_available_slots(data, target_date_str):
    '''
    data["booked"]
    '''
    booked_slots = {b["slot"] for b in data["booked"] if b["dated"] == target_date_str}

    # Determine which timing to use: special or regular
    special = data.get("sp", {})
    use_special = special and special.get("sdate") == target_date_str and not special.get("off")
    
    if use_special:
        time_range = special["hours"]
    else:
        wd_map = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        date_obj = datetime.strptime(target_date_str, "%Y-%m-%d")
        wd = wd_map[date_obj.weekday()]
        time_range = data["hours"].get(wd, "00:00-00:00#0")

    time_part = time_range.split('#')[0]
    if time_part == "00:00-00:00":
        return []  # Doctor not available that day

    start_str, end_str = time_part.split("-")
    start_time = datetime.strptime(start_str, "%H:%M")
    end_time = datetime.strptime(end_str, "%H:%M")

    slots = []
    current = start_time
    while current + timedelta(minutes=30) <= end_time:
        slot = f"{current.strftime('%H:%M')}-{(current + timedelta(minutes=30)).strftime('%H:%M')}"
        if slot not in booked_slots:
            slots.append(slot)
            
        current += timedelta(minutes=30)
    return slots
    #return {'slots':slots,'timezone':SERVER_TZ}
@router.get("/doctorq/{id}")      
def doctorq(id:int,dat:Optional[str]=None,db:Session=Depends(get_db)):  
    if id!=None:
        d=db.query(DoctorQ).filter(DoctorQ.id==id,DoctorQ.is_active==1).first()
       
        return {'info':d}


@router.get("/schedule/{id}")      
def schedule(id:int,dat:Optional[str]=None,db:Session=Depends(get_db)):

       if(dat==None ):
          dat=str(datetime.today()).split(" ")[0]
        
       dt =datetime.strptime(dat,'%Y-%m-%d') 
       n1=datetime.now()  
       n1=n1+timedelta(seconds=SERVER_OFFSET+BOOKING_GAP)
       n=5
       max_date=n1+timedelta(days=n)
       max_date=str(max_date).split(' ')[0]
       min_date=str(n1).split(' ')[0]
       start_hours=str(n1).split(' ')[1]
       max_datef=datetime.strptime(max_date,'%Y-%m-%d')
       min_datef=datetime.strptime(min_date,'%Y-%m-%d')
       ret={}
       if dt >max_datef or dt <min_datef:
            
            routine={'hours':"00:00-00:00"}
            return {'routine':routine,'book':'','spoff':'','sp':''}
          #return JsonResponse({'routine': "hours": "00:00-00:00",,'book':obj2,'spoff':spoff,'sp':spstring})
      
       # WHEN IN WITHIN RANGE
       #print(str(dt)[0:10])
       #print(min_date)
       if(str(dt)[0:10]==min_date):
           st=start_hours.split(':')
           sthr=int(st[0])
           stmin=int(st[1])
           if(stmin<30):
               stmin=30
               sthr=st[0]
           else:
               stmin=00
               sthr=int(sthr)+1    
           ret['sthour']=sthr
           ret['stmin']=stmin

       wd=dt.weekday()
       ret['wd']=wd
       d=db.query(Doctor).filter(Doctor.id==id).first()
       sp=db.query(DoctorSpecial).join(Doctor ,DoctorSpecial.doctor_id==Doctor.id).filter(DoctorSpecial.sdate==dt).filter(DoctorSpecial.doctor_id==id).first()
       booked=db.query(Book).join(Doctor ,Book.doctor_id==Doctor.id).filter(Book.dated==dt).filter(Book.doctor_id==id).filter(Book.status=='BOOKED').all()
       
       if(d!=None ):
         ret['hours']=d
       if(sp!=None) :
           ret['sp']=sp 
       if(booked):
           ret['booked']=booked
       return ret    