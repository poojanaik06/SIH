from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter()

@router.post("/areas/", response_model=schemas.Area)
def create_area(
    area: schemas.AreaCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_or_create_area(db=db, area_name=area.area_name)

@router.post("/crops/", response_model=schemas.Crop)
def create_crop(
    crop: schemas.CropCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_or_create_crop(db=db, crop_name=crop.crop_name)

@router.post("/data/yield/")
def create_yield_data(
    data: schemas.YieldDataCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_data_record(db, data, models.YieldData)

# Add similar endpoints for rainfall, temperature, and pesticide data