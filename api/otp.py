from fastapi import APIRouter, HTTPException
from fastapi import APIRouter,Depends,Path
from datetime import datetime, timedelta
import random, smtplib
from sqlalchemy.orm import Session
from email.mime.text import MIMEText
from models.category import EmailOTP
from core.database import get_db
router = APIRouter()

def send_email_otp(email: str, otp: str):
    sender = "no-reply@example.com"
    subject = "Your OTP Code"
    body = f"Your verification code is: {otp}. It will expire in 10 minutes."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = email

    with smtplib.SMTP("smtp.yourprovider.com", 587) as server:
        server.starttls()
        server.login("your_smtp_user", "your_smtp_password")
        server.sendmail(sender, email, msg.as_string())

@router.post("/send-email-otp")
async def send_email_otp_route(email: str):
    otp = str(random.randint(100000, 999999))  # 6-digit OTP
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Save to DB or Redis
    # db.add(EmailOTP(email=email, otp_code=otp, expires_at=expires_at))
    # db.commit()

    send_email_otp(email, otp)
    return {"message": "OTP sent to email"}
@router.post("/verify-email-otp")
async def verify_email_otp(email: str, otp: str,db: Session = Depends(get_db)):
    otp_entry = db.query(EmailOTP).filter_by(email=email, is_used=False).order_by(EmailOTP.id.desc()).first()

    if not otp_entry:
        raise HTTPException(status_code=400, detail="No OTP found or expired")

    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    if otp_entry.otp_code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    otp_entry.is_used = True
    # db.commit()

    return {"message": "Email verified successfully"}

