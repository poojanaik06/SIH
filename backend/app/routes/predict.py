import os
import sys
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..ml_service import get_ml_service
from datetime import datetime
import logging

# Add ML model utils to path for weather fetching
ml_model_path = Path(__file__).parent.parent.parent / "ml-model"
sys.path.append(str(ml_model_path))

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/enhanced", response_model=schemas.PredictionOutput)
def create_enhanced_prediction(
    payload: schemas.PredictionInput,
    db: Session = Depends(get_db)
):
    """Create an enhanced crop yield prediction with automatic weather fetching"""
    try:
        # Get ML service
        ml_service = get_ml_service()
        
        if not ml_service.is_loaded:
            raise HTTPException(status_code=500, detail="ML model not loaded")
        
        # Import weather fetching utilities
        try:
            from utils.weather_fetcher import get_weather_data_for_location, get_weather_data_for_region
        except ImportError:
            logger.warning("Weather fetching utilities not available, using fallback")
            # Fallback function
            def get_weather_data_for_location(location, year=None):
                return {
                    'avg_temp': 25.0,
                    'average_rain_fall_mm_per_year': 800.0,
                    'humidity': 65.0,
                    'sunshine_hours': 7.0
                }
            def get_weather_data_for_region(location, year=None):
                return get_weather_data_for_location(location, year)
        
        # Determine location
        location = payload.location or payload.area_name
        if not location:
            raise HTTPException(status_code=400, detail="Either 'location' or 'area_name' must be provided")
        
        # Use current year if not provided
        year = payload.year or datetime.now().year
        
        # Fetch weather data automatically
        logger.info(f"Fetching weather data for location: {location}, year: {year}")
        try:
            weather_data = get_weather_data_for_location(location, year)
        except Exception as e:
            logger.warning(f"Weather API failed: {e}, using regional fallback")
            # Try regional approach as fallback
            try:
                weather_data = get_weather_data_for_region(location, year)
            except:
                # Final fallback to defaults
                weather_data = {
                    'avg_temp': 25.0,
                    'average_rain_fall_mm_per_year': 800.0,
                    'humidity': 65.0,
                    'sunshine_hours': 7.0
                }
        
        # Get regional defaults for soil parameters
        regional_defaults = get_regional_defaults(location)
        
        # Prepare enhanced input data
        input_data = {
            'Area': location,
            'Item': payload.crop_name,
            'Year': year,
            'average_rain_fall_mm_per_year': payload.rainfall_mm or weather_data.get('average_rain_fall_mm_per_year', 800.0),
            'avg_temp': payload.avg_temp or weather_data.get('avg_temp', 25.0),
            'pesticides_tonnes': payload.pesticide_tonnes or regional_defaults.get('pesticides_tonnes', 100.0),
            'humidity': payload.humidity or weather_data.get('humidity', 65.0),
            'nitrogen': payload.nitrogen or regional_defaults.get('nitrogen', 80.0),
            'phosphorus': payload.phosphorus or regional_defaults.get('phosphorus', 40.0),
            'potassium': payload.potassium or regional_defaults.get('potassium', 60.0),
            'soil_ph': payload.soil_ph or regional_defaults.get('soil_ph', 6.5),
            'ndvi_avg': payload.ndvi_avg or regional_defaults.get('ndvi_avg', 0.75),
            'organic_matter': payload.organic_matter or regional_defaults.get('organic_matter', 3.0)
        }
        
        # Make prediction
        prediction_result = ml_service.predict(input_data)
        
        if not prediction_result['success']:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {prediction_result['error']}")
        
        predicted_yield = prediction_result['predicted_yield']
        
        # Log the prediction
        logger.info(f"Enhanced prediction made: Location: {location}, Crop: {payload.crop_name}, Yield: {predicted_yield}")
        
        return schemas.PredictionOutput(
            predicted_yield=predicted_yield,
            unit=prediction_result.get('unit', 'hg/ha'),
            confidence=prediction_result.get('confidence', 'high'),
            model_info={
                'weather_data_source': 'Open-Meteo API',
                'location_geocoded': location,
                'weather_fetched': True,
                'regional_defaults_applied': True,
                **prediction_result.get('model_info', {})
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_regional_defaults(location: str) -> dict:
    """Get regional default values for soil and agricultural parameters"""
    # Enhanced regional defaults based on farmer_friendly_predict.py
    regional_defaults = {
        'India': {
            'soil_ph': 7.0,
            'nitrogen': 250.0,  # kg/hectare
            'phosphorus': 25.0,  # kg/hectare
            'potassium': 200.0,  # kg/hectare
            'organic_matter': 1.0,  # percentage
            'humidity': 65.0,  # percentage
            'sunshine_hours': 8.0,  # hours per day
            'elevation': 200.0,  # meters
            'ndvi_avg': 0.65,  # Normalized Difference Vegetation Index
            'pesticides_tonnes': 120.0,  # tonnes
        },
        'USA': {
            'soil_ph': 6.5,
            'nitrogen': 150.0,
            'phosphorus': 40.0,
            'potassium': 200.0,
            'organic_matter': 2.5,
            'humidity': 60.0,
            'sunshine_hours': 7.5,
            'elevation': 500.0,
            'ndvi_avg': 0.70,
            'pesticides_tonnes': 150.0,
        },
        'China': {
            'soil_ph': 7.5,
            'nitrogen': 200.0,
            'phosphorus': 35.0,
            'potassium': 180.0,
            'organic_matter': 1.8,
            'humidity': 62.0,
            'sunshine_hours': 7.0,
            'elevation': 800.0,
            'ndvi_avg': 0.68,
            'pesticides_tonnes': 130.0,
        },
        'Brazil': {
            'soil_ph': 5.5,
            'nitrogen': 120.0,
            'phosphorus': 30.0,
            'potassium': 150.0,
            'organic_matter': 2.2,
            'humidity': 75.0,
            'sunshine_hours': 6.5,
            'elevation': 300.0,
            'ndvi_avg': 0.72,
            'pesticides_tonnes': 110.0,
        },
        'Australia': {
            'soil_ph': 7.2,
            'nitrogen': 100.0,
            'phosphorus': 20.0,
            'potassium': 120.0,
            'organic_matter': 1.5,
            'humidity': 55.0,
            'sunshine_hours': 9.0,
            'elevation': 400.0,
            'ndvi_avg': 0.60,
            'pesticides_tonnes': 90.0,
        },
        'Canada': {
            'soil_ph': 6.8,
            'nitrogen': 180.0,
            'phosphorus': 45.0,
            'potassium': 220.0,
            'organic_matter': 3.0,
            'humidity': 68.0,
            'sunshine_hours': 6.0,
            'elevation': 600.0,
            'ndvi_avg': 0.66,
            'pesticides_tonnes': 140.0,
        },
        'Russia': {
            'soil_ph': 6.0,
            'nitrogen': 90.0,
            'phosphorus': 25.0,
            'potassium': 160.0,
            'organic_matter': 2.8,
            'humidity': 70.0,
            'sunshine_hours': 5.5,
            'elevation': 1000.0,
            'ndvi_avg': 0.58,
            'pesticides_tonnes': 80.0,
        }
    }
    
    # Default values for any other region
    default_values = {
        'soil_ph': 6.5,
        'nitrogen': 150.0,
        'phosphorus': 30.0,
        'potassium': 150.0,
        'organic_matter': 2.0,
        'humidity': 65.0,
        'sunshine_hours': 7.0,
        'elevation': 500.0,
        'ndvi_avg': 0.65,
        'pesticides_tonnes': 120.0,
    }
    
    # Try to match region from location string
    location_lower = location.lower()
    
    for region, defaults in regional_defaults.items():
        if region.lower() in location_lower:
            return defaults
    
    # If no specific region matched, return defaults
    return default_values

@router.post("/farmer-friendly", response_model=schemas.PredictionOutput)
def create_farmer_friendly_prediction(
    payload: schemas.PredictionInput,
    db: Session = Depends(get_db)
):
    """Create a farmer-friendly prediction using the same logic as farmers_predict.py"""
    try:
        # Import the exact same prediction function used by farmers_predict.py
        try:
            # Add the ML model directory to Python path for imports
            import sys
            from pathlib import Path
            ml_model_path = Path(__file__).parent.parent.parent / "ml-model"
            if str(ml_model_path) not in sys.path:
                sys.path.append(str(ml_model_path))
            
            from farmer_friendly_predict import predict_yield_farmer_friendly
        except ImportError as e:
            logger.error(f"farmer_friendly_predict module import failed: {e}")
            raise HTTPException(status_code=500, detail="Farmer prediction module not available")
        
        # Determine location
        location = payload.location or payload.area_name
        if not location:
            raise HTTPException(status_code=400, detail="Either 'location' or 'area_name' must be provided")
        
        # Use current year if not provided
        year = payload.year or datetime.now().year
        
        # Prepare input data in the same format as farmers_predict.py
        farmer_data = {
            "Area": location,
            "Item": payload.crop_name,
            "Year": year,
            # Determine area type (specific location vs region)
            "area_type": "location" if ',' in location else "country"
        }
        
        # Add optional parameters if provided by user
        if payload.avg_temp is not None:
            farmer_data["avg_temp"] = payload.avg_temp
        if payload.rainfall_mm is not None:
            farmer_data["average_rain_fall_mm_per_year"] = payload.rainfall_mm
        if payload.humidity is not None:
            farmer_data["humidity"] = payload.humidity
        if payload.nitrogen is not None:
            farmer_data["nitrogen"] = payload.nitrogen
        if payload.phosphorus is not None:
            farmer_data["phosphorus"] = payload.phosphorus
        if payload.potassium is not None:
            farmer_data["potassium"] = payload.potassium
        if payload.soil_ph is not None:
            farmer_data["soil_ph"] = payload.soil_ph
        if payload.ndvi_avg is not None:
            farmer_data["ndvi_avg"] = payload.ndvi_avg
        if payload.organic_matter is not None:
            farmer_data["organic_matter"] = payload.organic_matter
        if payload.pesticide_tonnes is not None:
            farmer_data["pesticides_tonnes"] = payload.pesticide_tonnes
        
        # Make prediction using the EXACT same function as farmers_predict.py
        logger.info(f"Making farmer-friendly prediction for {location}, {payload.crop_name}")
        prediction_result = predict_yield_farmer_friendly(farmer_data)
        
        if not prediction_result['success']:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {prediction_result['error']}")
        
        predicted_yield = prediction_result['predicted_yield']
        defaulted_parameters = prediction_result.get('defaulted_parameters', [])
        auto_fetched_weather = prediction_result.get('auto_fetched_weather', [])
        
        # Log the farmer-friendly prediction
        logger.info(f"Farmer-friendly prediction: Location: {location}, Crop: {payload.crop_name}, Yield: {predicted_yield}")
        logger.info(f"Defaulted parameters: {defaulted_parameters}")
        logger.info(f"Auto-fetched weather: {auto_fetched_weather}")
        
        return schemas.PredictionOutput(
            predicted_yield=predicted_yield,
            unit=prediction_result.get('unit', 'hg/ha'),
            confidence='high',  # Since we're using the same model as farmers_predict.py
            model_info={
                'prediction_type': 'farmer_friendly_direct',
                'weather_data_source': 'Open-Meteo API' if auto_fetched_weather else 'Regional Defaults',
                'location_geocoded': location,
                'weather_fetched': len(auto_fetched_weather) > 0,
                'regional_defaults_applied': len(defaulted_parameters) > 0,
                'defaulted_parameters': defaulted_parameters,
                'auto_fetched_weather': auto_fetched_weather,
                'region_used': prediction_result.get('region_used', location),
                'yield_tonnes_per_hectare': round(predicted_yield / 10000, 2),
                'yield_bushels_per_acre': round(predicted_yield * 0.0143, 1),
                'using_same_model_as_cli': True,
                'model_source': 'farmer_friendly_predict.py'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Farmer-friendly prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
def create_prediction(
    payload: schemas.PredictionInput,
    db: Session = Depends(get_db)
):
    """Create a crop yield prediction - uses enhanced prediction with weather API"""
    # For backwards compatibility, redirect to enhanced prediction
    return create_enhanced_prediction(payload, db)

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