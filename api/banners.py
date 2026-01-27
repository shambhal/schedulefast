from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.category import Banner,Category
router = APIRouter()
from pydantic import BaseModel
from typing import Optional

class BannerBase(BaseModel):
    category_id: int
    sort_order: int = 0
    image: Optional[str] = None  # path/URL of image
    tag:Optional[str]=None
    category:Optional[dict]=None
class BannerCreate(BannerBase):
    pass

class BannerUpdate(BaseModel):
    sort_order: Optional[int] = None
    image: Optional[str] = None

class BannerOut(BannerBase):
    id: int

    class Config:
        orm_mode = True


@router.get("/", response_model=list[BannerOut])
def get_banners(db: Session = Depends(get_db)):
    """
    Return all banners sorted by sort_order
    """
    banners = db.query(Banner).order_by(Banner.sort_order).all()
    return banners
@router.get("/by_tag/", response_model=list[BannerOut])
def get_banners_by_tag(
    tag: str = Query(...),
    db: Session = Depends(get_db)
):
    banners = (
        db.query(Banner)
        .filter(Banner.tag == tag)
        .order_by(Banner.sort_order)
        .all()
    )

    bms = []

    for banner in banners:
        temp = banner.__dict__.copy()
        temp.pop("_sa_instance_state", None)

        if banner.category_id:
            cat = db.query(Category).filter(Category.id == banner.category_id).first()
            if cat:
                cat_dict = cat.__dict__.copy()
                cat_dict.pop("_sa_instance_state", None)
                print(cat_dict)
                temp["category"] = cat_dict
                print(temp)
            else:
                temp["category"] = None
        else:
            temp["category"] = None

        bms.append(temp)
        #print(bms)
    return bms
