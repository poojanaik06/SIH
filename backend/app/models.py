from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    farm_size = Column(String(50), nullable=True)

class Area(Base):
    __tablename__ = "areas"
    area_id = Column(Integer, primary_key=True, index=True)
    area_name = Column(String(100), nullable=False, unique=True)

class Crop(Base):
    __tablename__ = "crops"
    crop_id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(100), nullable=False, unique=True)

class YieldData(Base):
    __tablename__ = "yield_data"
    yield_id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.area_id"))
    crop_id = Column(Integer, ForeignKey("crops.crop_id"))
    year = Column(Integer, nullable=False)
    yield_value = Column(DECIMAL(10, 2))
    unit = Column(String(20))
    area = relationship("Area")
    crop = relationship("Crop")

class RainfallData(Base):
    __tablename__ = "rainfall_data"
    rainfall_id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.area_id"))
    year = Column(Integer, nullable=False)
    rainfall_mm = Column(DECIMAL(8, 2))
    area = relationship("Area")

class TemperatureData(Base):
    __tablename__ = "temperature_data"
    temp_id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.area_id"))
    year = Column(Integer, nullable=False)
    avg_temp = Column(DECIMAL(5, 2))
    area = relationship("Area")

class PesticideData(Base):
    __tablename__ = "pesticide_data"
    pesticide_id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.area_id"))
    year = Column(Integer, nullable=False)
    pesticide_tonnes = Column(DECIMAL(10, 2))
    area = relationship("Area")