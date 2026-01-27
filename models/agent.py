from fastapi import date
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.database import get_db
from models.category import Category
class AgentDoctorQuery(BaseModel):
    category: str
    from_date: date
    to_date: date
    preferred_slots: list[str] | None = None
   
def doctor_agent(query1:AgentDoctorQuery,db) :
     cat_id=db.query(Category).filter(
        Category.name.ilike(query1.name)   # case-insensitive
      ).first()
     if not cat_id :
          
    
          return []     
     if query1.preferred_slots:
          
          pass
     else:
          pass
          
