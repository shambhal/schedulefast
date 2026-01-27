from fastapi import APIRouter,HTTPException,Request,Response
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey,UniqueConstraint,Date,Numeric
import random
from  datetime import datetime,timedelta
from sqlalchemy.orm import Session
from core.database import get_db
from models.category import Doctor,DoctorSpecial,Book
from forms.contactform import ContactForm
from fastapi.responses import JSONResponse
router = APIRouter()
@router.get('/captcha')
def gencaptcha(request:Request,response:Response):
   operator=random.choice(['+','*'])
   num1=random.randint(2,5)
   num2=random.randint(2,8)
   expression=f'{num1} {operator} {num2}'
   result=eval(expression)
   expression=expression.replace("*",'X')
   response.set_cookie(key="captcha",value=result,httponly=True)
   #response.set_cookie(key="user_id", value="abc123", httponly=True)
   return JSONResponse(content={"captcha": expression})  # Replace with actual image
from fastapi import Form

@router.post("/contact")

def contact(request: Request, form: ContactForm):
    expected = request.cookies.get("captcha")
    if expected is None:
        raise HTTPException(status_code=400, detail="Captcha cookie missing")

    if form.captcha_input.strip() != expected:
        raise HTTPException(status_code=400, detail="Captcha answer is incorrect")

    # Proceed to handle form data (store/email/send etc.)
    return {"message": "Message sent successfully"}



def getSlotPrice(doc_id: int, slot: str, dt: str, db: Session) -> int:
    # Convert string to datetime
    date_obj = datetime.strptime(dt, "%Y-%m-%d")
    weekday = date_obj.weekday()
    wd_map = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    weekday_name = wd_map[weekday]

    # Get doctor details
    doctor = db.query(Doctor).filter(Doctor.id == doc_id).first()
    if not doctor:
        raise ValueError("Doctor not found")

    # Get special pricing if exists
    special = (
        db.query(DoctorSpecial)
        .filter(DoctorSpecial.doctor_id == doc_id, DoctorSpecial.sdate == dt)
        .first()
    )

    if special:
        hours_str = special.hours  # e.g., "10:00-14:00#800"
    else:
        hours_str = getattr(doctor,weekday_name, "00:00-00:00#600")  # fallback default
    #print(hours_str)
    #print(doctor)
    # Parse time range and price
    if "#" in hours_str:
        time_part, fee = hours_str.split("#")
    else:
        time_part = hours_str
        fee = "600"  # fallback fee

    # Check if slot is in valid time range
    start_str, end_str = time_part.split("-")
    start_time = datetime.strptime(start_str, "%H:%M")
    end_time = datetime.strptime(end_str, "%H:%M")

    current = start_time
    #print(start_time)
    #print(end_time)
    while current + timedelta(minutes=30) <= end_time:
        slot_str = current.strftime("%H:%M")
        #print(slot_str)
        #print(slot)
        #print(slot[0:5])
        if slot_str == slot[0:5]:
            return int(fee)
        current += timedelta(minutes=30)

    # If slot not found in valid range
    raise ValueError("Invalid slot or slot not available")
