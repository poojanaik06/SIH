import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..ml_service import get_ml_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=schemas.PredictionOutput)
def create_prediction(
    payload: schemas.PredictionInput,
    db: Session = Depends(get_db)
):
    """Create a crop yield prediction using the integrated ML model"""
    try:
        # Get ML service
        ml_service = get_ml_service()
        
        if not ml_service.is_loaded:
            raise HTTPException(status_code=500, detail="ML model not loaded")
        
        # Prepare input data for the ML model
        input_data = {
            'Area': payload.area_name,
            'Item': payload.crop_name,
            'Year': payload.year,
            'average_rain_fall_mm_per_year': payload.rainfall_mm,
            'avg_temp': payload.avg_temp,
            'pesticides_tonnes': payload.pesticide_tonnes
        }
        
        # Make prediction
        prediction_result = ml_service.predict(input_data)
        
        if not prediction_result['success']:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {prediction_result['error']}")
        
        predicted_yield = prediction_result['predicted_yield']
        
        # Store prediction in database (optional - for history tracking)
        try:
            # Find or create area and crop entries
            area = db.query(models.Area).filter(models.Area.area_name == payload.area_name).first()
            if not area:
                area = models.Area(area_name=payload.area_name)
                db.add(area)
                db.flush()
            
            crop = db.query(models.Crop).filter(models.Crop.crop_name == payload.crop_name).first()
            if not crop:
                crop = models.Crop(crop_name=payload.crop_name)
                db.add(crop)
                db.flush()
            
            # Store the prediction (you might want to create a predictions table)
            # For now, we'll just log it
            logger.info(f"Prediction made: Area: {payload.area_name}, Crop: {payload.crop_name}, Yield: {predicted_yield}")
            
            db.commit()
        except Exception as db_error:
            logger.warning(f"Database storage failed: {db_error}")
            db.rollback()
            # Continue even if DB storage fails
        
        return schemas.PredictionOutput(
            predicted_yield=predicted_yield,
            unit=prediction_result.get('unit', 'hg/ha')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/batch", response_model=list[schemas.PredictionOutput])
def create_batch_predictions(
    payloads: list[schemas.PredictionInput],
    db: Session = Depends(get_db)
):
    """Create multiple crop yield predictions"""
    try:
        ml_service = get_ml_service()
        
        if not ml_service.is_loaded:
            raise HTTPException(status_code=500, detail="ML model not loaded")
        
        results = []
        
        for payload in payloads:
            input_data = {
                'Area': payload.area_name,
                'Item': payload.crop_name, 
                'Year': payload.year,
                'average_rain_fall_mm_per_year': payload.rainfall_mm,
                'avg_temp': payload.avg_temp,
                'pesticides_tonnes': payload.pesticide_tonnes
            }
            
            prediction_result = ml_service.predict(input_data)
            
            if prediction_result['success']:
                results.append(schemas.PredictionOutput(
                    predicted_yield=prediction_result['predicted_yield'],
                    unit=prediction_result.get('unit', 'hg/ha')
                ))
            else:
                # For batch processing, we might want to continue with other predictions
                logger.warning(f"Batch prediction failed for {payload.area_name}, {payload.crop_name}: {prediction_result['error']}")
                results.append(schemas.PredictionOutput(
                    predicted_yield=0.0,
                    unit="error"
                ))
        
        return results
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@router.get("/model-info")
def get_model_info():
    """Get information about the loaded ML model"""
    ml_service = get_ml_service()
    return ml_service.get_model_info()

@router.get("/health")
def health_check():
    """Health check for the prediction service"""
    ml_service = get_ml_service()
    return {
        'status': 'healthy',
        'ml_model_loaded': ml_service.is_loaded,
        'timestamp': datetime.now().isoformat()
    }