from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash

# --- User CRUD ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Data Management CRUD ---
def get_or_create_area(db: Session, area_name: str):
    area = db.query(models.Area).filter(models.Area.area_name == area_name).first()
    if not area:
        area = models.Area(area_name=area_name)
        db.add(area)
        db.commit()
        db.refresh(area)
    return area

def get_or_create_crop(db: Session, crop_name: str):
    crop = db.query(models.Crop).filter(models.Crop.crop_name == crop_name).first()
    if not crop:
        crop = models.Crop(crop_name=crop_name)
        db.add(crop)
        db.commit()
        db.refresh(crop)
    return crop

def create_data_record(db: Session, record_data, model_class):
    db_record = model_class(**record_data.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record