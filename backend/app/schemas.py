from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Base and Create Schemas ---
class AreaBase(BaseModel):
    area_name: str
class AreaCreate(AreaBase):
    pass

class CropBase(BaseModel):
    crop_name: str
class CropCreate(CropBase):
    pass

class YieldDataBase(BaseModel):
    area_id: int
    crop_id: int
    year: int
    yield_value: float
    unit: str
class YieldDataCreate(YieldDataBase):
    pass

class RainfallDataBase(BaseModel):
    area_id: int
    year: int
    rainfall_mm: float
class RainfallDataCreate(RainfallDataBase):
    pass

class TemperatureDataBase(BaseModel):
    area_id: int
    year: int
    avg_temp: float
class TemperatureDataCreate(TemperatureDataBase):
    pass

class PesticideDataBase(BaseModel):
    area_id: int
    year: int
    pesticide_tonnes: float
class PesticideDataCreate(PesticideDataBase):
    pass

# --- Full Schemas for Reading Data ---
class Area(AreaBase):
    area_id: int
    class Config: from_attributes = True

class Crop(CropBase):
    crop_id: int
    class Config: from_attributes = True

# (You can create full schemas for other data types if needed)

# --- User and Auth Schemas (Mostly unchanged) ---
class UserBase(BaseModel):
    email: EmailStr
class UserCreate(UserBase):
    password: str
class User(UserBase):
    id: int
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    email: Optional[str] = None

# --- Prediction Schemas (Updated) ---
class PredictionInput(BaseModel):
    area_name: str
    crop_name: str
    year: int
    avg_temp: float
    rainfall_mm: float
    pesticide_tonnes: float

class PredictionOutput(BaseModel):
    predicted_yield: float
    unit: str = "hg/ha"
    confidence: Optional[str] = "high"
    model_info: Optional[dict] = None