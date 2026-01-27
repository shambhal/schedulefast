from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from models.category import Config
from core.database import get_db

from pydantic import BaseModel

class ConfigV(BaseModel):
    cname: str
    cvalue: str
    class Config:
        orm_mode = True  # Pydantic v2
router = APIRouter()
@router.get("/settings", response_model=list[ConfigV])

def getBasicSettings(db: Session = Depends(get_db)):
    rows = db.query(Config.cname,Config.cvalue).all()
    return rows
