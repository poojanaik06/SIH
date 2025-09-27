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

# --- User and Auth Schemas (Updated for Registration) ---
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    farm_size: Optional[str] = None

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

# --- Prediction Schemas (Updated for Advanced ML Model) ---
class PredictionInput(BaseModel):
    # Required fields
    location: str  # Any location string (e.g., "Karnataka, India", "New York, USA")
    crop_name: str
    
    # Optional fields (system will use defaults or fetch from APIs)
    year: Optional[int] = None  # Will use current year if not provided
    
    # Advanced optional fields for better predictions
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    soil_ph: Optional[float] = None
    humidity: Optional[float] = None
    ndvi_avg: Optional[float] = None
    organic_matter: Optional[float] = None
    
    # Legacy support for backwards compatibility
    area_name: Optional[str] = None  # Will map to location if provided
    avg_temp: Optional[float] = None  # Will be fetched from weather API
    rainfall_mm: Optional[float] = None  # Will be fetched from weather API
    pesticide_tonnes: Optional[float] = None  # Will use regional default

class PredictionOutput(BaseModel):
    predicted_yield: float
    unit: str = "hg/ha"
    confidence: Optional[str] = "high"
    model_info: Optional[dict] = None