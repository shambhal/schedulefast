from fastapi import APIRouter,Depends,Path
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import SECRET_KEY,ALGORITHM
from typing import Optional
import datetime
from datetime import timedelta,timezone
from models.category import User,Customer,Order

from forms import customerform
from fastapi import FastAPI, HTTPException,Request
from fastapi.responses import JSONResponse
from jose import jwt
router=APIRouter()
def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Optional: Check expiry manually if needed
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
            return None
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid (wrong secret, malformed, etc.)
        return None
@router.get('/info')
def get_userinfo(request: Request, db: Session = Depends(get_db)):
    # Get token from cookies (or from Authorization header)
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

    # Build response
    customer = user.customer
    userinfo = {
        "id": user.id,
        "email": user.email,
        "name": f"{user.first_name} {user.last_name}".strip(),
        "phone": customer.phone if customer else None
    }

    return JSONResponse(content=userinfo)
