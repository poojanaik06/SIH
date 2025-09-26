from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
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

@router.get("/combined-dataset")
def get_combined_dataset(
    limit: int = 100,
    offset: int = 0,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get data from the combined_dataset view"""
    try:
        # Query the combined dataset view
        query = text("""
            SELECT 
                area_name,
                crop_name,
                year,
                yield_value,
                unit,
                rainfall_mm,
                avg_temp,
                pesticide_tonnes
            FROM combined_dataset
            ORDER BY area_name, crop_name, year
            LIMIT :limit OFFSET :offset
        """)
        
        result = db.execute(query, {"limit": limit, "offset": offset})
        rows = result.fetchall()
        
        # Convert to list of dictionaries
        data = []
        for row in rows:
            data.append({
                "area_name": row[0],
                "crop_name": row[1],
                "year": row[2],
                "yield_value": float(row[3]) if row[3] else None,
                "unit": row[4],
                "rainfall_mm": float(row[5]) if row[5] else None,
                "avg_temp": float(row[6]) if row[6] else None,
                "pesticide_tonnes": float(row[7]) if row[7] else None
            })
        
        # Get total count
        count_query = text("SELECT COUNT(*) FROM combined_dataset")
        total_count = db.execute(count_query).scalar()
        
        return {
            "success": True,
            "data": data,
            "total_count": total_count,
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/combined-dataset/summary")
def get_dataset_summary(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get summary statistics from the combined dataset"""
    try:
        # Get summary statistics
        query = text("""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT area_name) as unique_areas,
                COUNT(DISTINCT crop_name) as unique_crops,
                MIN(year) as min_year,
                MAX(year) as max_year,
                AVG(yield_value) as avg_yield,
                AVG(rainfall_mm) as avg_rainfall,
                AVG(avg_temp) as avg_temperature,
                AVG(pesticide_tonnes) as avg_pesticides
            FROM combined_dataset
            WHERE yield_value IS NOT NULL
        """)
        
        result = db.execute(query)
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="No data found in combined dataset")
        
        summary = {
            "total_records": row[0] or 0,
            "unique_areas": row[1] or 0,
            "unique_crops": row[2] or 0,
            "year_range": {"min": row[3] or 0, "max": row[4] or 0},
            "averages": {
                "yield_value": round(float(row[5]), 2) if row[5] else 0,
                "rainfall_mm": round(float(row[6]), 2) if row[6] else 0,
                "avg_temp": round(float(row[7]), 2) if row[7] else 0,
                "pesticide_tonnes": round(float(row[8]), 2) if row[8] else 0
            }
        }
        
        return {
            "success": True,
            "summary": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")