from fastapi import APIRouter,Depends,Path,HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import  SERVER_OFFSET,BOOKING_GAP
from typing import Optional
from  datetime import datetime,timedelta
from models.category import Information
router = APIRouter()
from pydantic import BaseModel
class InformationDetail(BaseModel):
    title: str
    seo_url: str
    content: str
    status: bool
    sort_order: int

    class Config:
        orm_mode = True

class InformationLink(BaseModel):
    title: str
    seo_url: str  # slug

    class Config:
        orm_mode = True
@router.get("/links", response_model=list[InformationLink])
def get_information_links(db: Session = Depends(get_db)):
    
    return (
        db.query(Information)
        .filter(Information.status == True)
        .order_by(Information.sort_order.asc())
        .with_entities(Information.seo_url, Information.title)
        .all()
    )

@router.get("/{slug}", response_model=InformationDetail)
def get_information_by_slug(slug: str, db: Session = Depends(get_db)):
    info = (
        db.query(Information)
        .filter(Information.seo_url == slug, Information.status == True)
        .first()
    )
    if not info:
        raise HTTPException(status_code=404, detail="Information not found")
    return info