from fastapi import APIRouter,Depends,Path
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import SECRET_KEY,ALGORITHM
from typing import Optional
import datetime
from datetime import timedelta
from models.category import User,Customer
from forms.customerform import CustomerResponse,UserResponse,UserCreate,UserLogin
from forms.guestform import GuestForm
from forms import customerform
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from passlib.hash import django_pbkdf2_sha256
from models.category import Category,Doctor,DoctorCategory
from jose import jwt
router=APIRouter()


@router.post("/guest-checkout")
async def guest_checkout(form: GuestForm):
    # Business logic here
    return {"success": True, "message": "Guest information saved!"}
@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # check existing email
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # check existing mobile
    '''
    if db.query(Customer).filter(Customer.phone == user_data.phone).first():
        raise HTTPException(status_code=400, detail="Mobile already registered")
    '''
    # create user
    hashed_password=django_pbkdf2_sha256.hash(user_data.password)
    user = User(
        username=user_data.email,
        email=user_data.email,
        
        first_name=user_data.name.split(' ')[0],
        last_name=user_data.name.split(' ')[1] if len(user_data.name.split(' '))>1 else '',
       
        password=hashed_password, 
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # create linked customer
    customer = Customer(
        user_id=user.id,
        phone=user_data.phone
    )
    db.add(customer)
    db.commit()
    access_token = create_token({"sub": user_data.email}, 30)   # 30 min
    refresh_token = create_token({"sub": user_data.email}, 60*24*7) # 7 days
    response=JSONResponse({'id':customer.id,'access_token':access_token,'refresh_token':refresh_token,'token':access_token,'customer_id':customer.id,'user_id':customer.user.id,'email':customer.user.email,'name':user_data.name,'phone':user_data.phone})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=1800
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 7
    )
    return response
    return customer
def create_token(data: dict, expires_minutes: int):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login(user: UserLogin,db: Session = Depends(get_db)):
    # after validating password...
    hashed_password=django_pbkdf2_sha256.hash(user.password)
    userobj=db.query(User).filter(User.username==user.email).filter(User.is_staff==0).first()
    
    if  userobj is None:
        return {'error':1,'msg':'Either customer is blocked or customer does not exist.'}
    k=django_pbkdf2_sha256.verify(user.password, userobj.password)
    
    if not k:
        return {'error':1,'msg':'Invalid Credentials'}
   # 30 min
    access_token = create_token({"sub": user.email}, 30)   # 30 min
    refresh_token = create_token({"sub": user.email}, 60*24*7) # 7 days
    if (customer := getattr(userobj, "customer", None)):
     phone = customer.phone
    else:
     phone = None
    dd={'id':customer.id,'user_id':customer.user.id,'name':userobj.first_name+ ' '+userobj.last_name,'email':userobj.email,'phone':phone,'refresh_token':refresh_token,'token':access_token,'access_token':access_token}
    response=JSONResponse(content=dd)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=1800
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 7
    )
    
    return response

@router.post("/refresh")
def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        new_access = create_token({"sub": email}, 30)
        return {"access_token": new_access}
    except:
        raise HTTPException(status_code=401, detail="Expired refresh token")
'''
@router.post("/guest-checkout")
async def guest_checkout(form: GuestForm):
    # Business logic here
    return {"success": True, "message": "Guest information saved!"}  
'''