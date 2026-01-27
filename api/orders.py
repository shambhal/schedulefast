from fastapi import APIRouter,Depends,Path,Request,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from core.config import  SERVER_OFFSET,BOOKING_GAP
from typing import Optional
from  datetime import datetime,timedelta
from forms.guestform import GuestForm,OrderUpdateForm,OrderStatusRequest
from models.category import OrderHistory,OrderItem,OrderTotal,Order,Category,Doctor
from .utils import getSlotPrice
router = APIRouter()
@router.post('/create')
def create(order:dict,request: Request,db:Session=Depends(get_db)):
 
    appointee=getattr(order,'appointee',None)
    user_agent = request.headers.get("user-agent")
    client_ip = request.client.host  # Optional: Get client IP
    if(appointee) :
     new_order = Order(
        name=order.appointee.name,
        email=order.appointee.email,
        phone=order.appointee.phone,
        payment_method=order.payment_method,
        device_id=order['device_id'],
        status="CREATED",
        user_agent=user_agent,
        total= order.total if order.total else 0,
        comment='',
        user_id=0,
        currency_code='INR'

     )
    else:
          new_order = Order(
        name='',
        email='',
        phone='',
        payment_method='',
        user_agent=user_agent,
        device_id=order['device_id'],
        status="CREATED",
        total=0,
        comment='',
        user_id=0,
        currency_code='INR'
     )


    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Add order items
    total=0
    for item in order['items']:
        price=getSlotPrice(item['doctor_id'],item['slot'],item['dated'],db)
        
        total +=price
        category=db.query(Category).filter(Category.id==item['category_id']).first()
        doctor=db.query(Doctor).filter(Doctor.id==item['doctor_id']).first()
        db_item = OrderItem(
            order_id=new_order.id,
            name=f"Appointment",
            quantity=1,
            category_id=item['category_id'],
            category=category.name if category!=None else '',
            doctor_id=item['doctor_id'],
            doctor=doctor.first_name +' '+doctor.last_name,
            slot=item['slot'],
            dated=item['dated'],
            price=price
        )
        total+=price
        db.add(db_item)
    new_order.total=total
    db.commit()

    return {"order_id": new_order.id}
@router.post('/update')


def updateAppointee(odf: OrderUpdateForm, db: Session = Depends(get_db)):
    try:
        existing_order = db.query(Order).filter(Order.id == odf.order_id).first()
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")

      
        if odf.appointee:
            existing_order.name = odf.appointee.name
            existing_order.email = odf.appointee.email
            existing_order.phone = odf.appointee.phone
        
        if odf.user_id is not None:
            existing_order.user_id = odf.user_id

        if odf.payment_method:
            existing_order.payment_method = odf.payment_method

        db.commit()
        db.refresh(existing_order)

        return {"id": existing_order.id, "message": "Appointee updated successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post('/validate')
def updatePM ( odf :OrderUpdateForm, db: Session = Depends(get_db)):
    # Find the order
    existing_order = db.query(Order).filter(Order.id ==odf.order_id).first()
    if not existing_order :
        raise HTTPException(status_code=404, detail="Order not found")
    if not odf.appointee :
        return{'error':'Missing Appointee details'}
    # Update fields from GuestForm (example)
   
    try:
        # Update appointee details
        
        if odf.appointee.name:
            existing_order.name = odf.appointee.name
        if odf.appointee.email:
            existing_order.email = odf.appointee.email
        if odf.appointee.phone:
            existing_order.phone = odf.appointee.phone

        # Update user_id if provided
        if odf.user_id is not None:
            existing_order.user_id = odf.user_id
           

        # Update payment method if provided
        if odf.payment_method:
           existing_order.payment_method = odf.payment_method

        db.commit()
        db.refresh(existing_order)
        #return {"id": existing_order.id, "message": "Appointee updated successfully"}
        return {"id": existing_order.id, "pmlink": "payments/"+odf.payment_method+'/getform'}
    except SQLAlchemyError as e:
        db.rollback()  # Important: reset session after failure
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
@router.post("/status")
def check_order_status(payload: OrderStatusRequest, db: Session = Depends(get_db)):
    """
    Check order status by order_id and email.
    """
    order = (
        db.query(Order)
        .filter(Order.id == payload.order_id, Order.email == payload.email)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found for this email.")

    return {"status": order.status}    
'''
@router.post('/process')
def updatePM ( odf :OrderUpdateForm, db: Session = Depends(get_db)):
    # Find the order
    existing_order = db.query(Order).filter(Order.id ==odf.order_id).first()
    if not existing_order :
        raise HTTPException(status_code=404, detail="Order not found")
    if not odf.appointee  :
        return{'error':'Missing Appointee details'}
    # Update fields from GuestForm (example)
   
    if(odf.appointee):
        existing_order.name = odf.appointee.name
        existing_order.email = odf.appointee.email
        existing_order.phone = odf.appointee.phone
    if(odf.user_id) :   
        existing_order.user_id=odf.user_id
    if(odf.payment_method) :
            existing_order.payment_method = odf.payment_method
    # Save changes
    #db.commit()
    #db.refresh(existing_order)

    return {"id": existing_order.id, "pmlink": "payments/"+odf.payment_method+'/getform'}
'''
