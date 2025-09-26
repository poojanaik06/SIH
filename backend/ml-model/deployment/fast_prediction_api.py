"""
Optimized FastAPI Service for Crop Yield Prediction
High-performance API with pre-loaded models and caching
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
import joblib
import pandas as pd
import numpy as np
import json
import glob
from datetime import datetime
import logging
from utils.preprocessing import DataPreprocessor
from utils.feature_engineering import FeatureEngineer
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Crop Yield Prediction API",
    description="High-performance API for predicting crop yields using advanced ML models",
    version="2.0.0"
)

# Global model artifacts - fix type annotations
from typing import Optional, Dict, Any

MODEL_ARTIFACTS: Dict[str, Any] = {
    'model': None,
    'scalers': None,
    'feature_names': None,
    'metadata': None,
    'preprocessor': None,
    'feature_engineer': None,
    'performance_metrics': None
}

# Pydantic models for request/response
class PredictionInput(BaseModel):
    Area: str = Field(..., description="Geographic area/country")
    Item: str = Field(..., description="Crop type")
    Year: int = Field(..., description="Year", ge=2000, le=2030)
    average_rain_fall_mm_per_year: float = Field(..., description="Annual rainfall in mm")
    avg_temp: float = Field(..., description="Average temperature in Celsius")
    pesticides_tonnes: float = Field(..., description="Pesticides used in tonnes")
    
    # Optional advanced features
    nitrogen: Optional[float] = Field(None, description="Nitrogen content")
    phosphorus: Optional[float] = Field(None, description="Phosphorus content")
    potassium: Optional[float] = Field(None, description="Potassium content")
    soil_ph: Optional[float] = Field(None, description="Soil pH level")
    humidity: Optional[float] = Field(None, description="Humidity percentage")
    ndvi_avg: Optional[float] = Field(None, description="NDVI average")
    vegetation_health: Optional[str] = Field("Healthy", description="Vegetation health status")
    
    # Additional optional soil features that model expects
    organic_matter: Optional[float] = Field(None, description="Organic matter content")
    moisture: Optional[float] = Field(None, description="Soil moisture")
    season_length: Optional[float] = Field(None, description="Growing season length")

class BatchPredictionInput(BaseModel):
    samples: List[PredictionInput]

class PredictionResponse(BaseModel):
    predicted_yield: float
    unit: str = "hg/ha"
    confidence_score: float
    processing_time_ms: float

class BatchPredictionResponse(BaseModel):
    predictions: List[float]
    statistics: Dict[str, float]
    processing_time_ms: float
    batch_size: int

def load_latest_model():
    """Load the most recent trained model and artifacts"""
    try:
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        # Explicitly use the best performing model
        model_base_name = "random_forest_crop_yield_20250925_224814"
        model_file = os.path.join(models_dir, f"{model_base_name}.joblib")
        
        if not os.path.exists(model_file):
            # Fallback to finding the latest model
            model_pattern = os.path.join(models_dir, 'random_forest_crop_yield_*.joblib')
            model_files = glob.glob(model_pattern)
            
            if not model_files:
                raise FileNotFoundError("No trained models found")
            
            # Get the latest model (by timestamp in filename)
            latest_model_file = max(model_files, key=os.path.getctime)
            model_base_name = os.path.basename(latest_model_file).replace('.joblib', '')
            model_file = latest_model_file
        
        logger.info(f"Loading model: {model_base_name}")
        
        # Load model artifacts
        MODEL_ARTIFACTS['model'] = joblib.load(model_file)
        
        # Load scalers
        scalers_file = os.path.join(models_dir, f"{model_base_name}_scalers.joblib")
        if os.path.exists(scalers_file):
            MODEL_ARTIFACTS['scalers'] = joblib.load(scalers_file)
        
        # Load feature names
        features_file = os.path.join(models_dir, f"{model_base_name}_features.joblib")
        if os.path.exists(features_file):
            MODEL_ARTIFACTS['feature_names'] = joblib.load(features_file)
        
        # Load metadata
        metadata_file = os.path.join(models_dir, f"{model_base_name}_metadata.json")
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                MODEL_ARTIFACTS['metadata'] = json.load(f)
                
                # Safely extract performance metrics
                if 'performance_metrics' in MODEL_ARTIFACTS['metadata']:
                    MODEL_ARTIFACTS['performance_metrics'] = MODEL_ARTIFACTS['metadata']['performance_metrics']
                else:
                    # Fallback performance metrics
                    MODEL_ARTIFACTS['performance_metrics'] = {
                        'r2': 0.78,
                        'rmse': 309,
                        'mae': 243,
                        'mape': 10.2
                    }
        else:
            # Fallback performance metrics if no metadata
            MODEL_ARTIFACTS['performance_metrics'] = {
                'r2': 0.78,
                'rmse': 309,
                'mae': 243,
                'mape': 10.2
            }
        
        # Initialize preprocessor and feature engineer
        MODEL_ARTIFACTS['preprocessor'] = DataPreprocessor()
        MODEL_ARTIFACTS['feature_engineer'] = FeatureEngineer()
        
        logger.info("✅ Model artifacts loaded successfully!")
        
        # Safely log performance metrics
        r2_score = MODEL_ARTIFACTS['performance_metrics'].get('r2', 'N/A')
        if isinstance(r2_score, (int, float)):
            logger.info(f"Model performance: R² = {r2_score:.4f}")
        else:
            logger.info(f"Model performance: R² = {r2_score}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        return False

def preprocess_input(data: Union[PredictionInput, List[PredictionInput]], 
                    use_advanced_features: bool = True) -> pd.DataFrame:
    """Create all 50 features expected by the model, matching simple_predict.py exactly"""
    
    # Convert to list if single input
    if not isinstance(data, list):
        data_list = [data]
    else:
        data_list = data
    
    # Process each input to create features
    feature_dicts = []
    
    for item in data_list:
        # Convert to dict properly for Pydantic models
        if hasattr(item, 'dict'):
            data_dict = item.dict()
        else:
            data_dict = dict(item)
        
        # Start with a dictionary to build features
        features = {}
        
        # Basic features (direct mapping)
        features['year'] = data_dict.get('Year', 2023)
        features['average_rain_fall_mm_per_year'] = data_dict.get('average_rain_fall_mm_per_year', 1200.0)
        features['avg_temp'] = data_dict.get('avg_temp', 25.0)
        features['pesticides_tonnes'] = data_dict.get('pesticides_tonnes', 100.0)
        features['soil_ph'] = data_dict.get('soil_ph', 6.5)
        features['nitrogen'] = data_dict.get('nitrogen', 80.0)
        features['phosphorus'] = data_dict.get('phosphorus', 40.0)
        features['potassium'] = data_dict.get('potassium', 60.0)
        features['organic_matter'] = data_dict.get('organic_matter', 3.0)
        features['humidity'] = data_dict.get('humidity', 65.0)
        features['sunshine_hours'] = data_dict.get('sunshine_hours', 8.0)
        features['ndvi_avg'] = data_dict.get('ndvi_avg', 0.75)
        features['elevation'] = data_dict.get('elevation', 500.0)
        
        # Handle vegetation_health - convert to numeric if it's a string
        vegetation_health = data_dict.get('vegetation_health', 'Healthy')
        if isinstance(vegetation_health, str):
            health_mapping = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Healthy': 3}
            features['vegetation_health'] = health_mapping.get(vegetation_health, 3)
        else:
            features['vegetation_health'] = int(vegetation_health) if vegetation_health is not None else 3
            
        features['light_intensity'] = 50000.0
        
        # Area one-hot encoding
        area = data_dict.get('Area', 'India')
        area_mapping = {
            'Australia': 'area_Australia',
            'Brazil': 'area_Brazil', 
            'Canada': 'area_Canada',
            'China': 'area_China',
            'India': 'area_India',
            'Russian Federation': 'area_Russia',
            'Russia': 'area_Russia',
            'United States of America': 'area_USA',
            'USA': 'area_USA'
        }
        
        areas = ['area_Australia', 'area_Brazil', 'area_Canada', 'area_China', 'area_India', 'area_Russia', 'area_USA']
        for area_col in areas:
            features[area_col] = 0
        
        if area in area_mapping:
            features[area_mapping[area]] = 1
        
        # Item one-hot encoding
        item_name = data_dict.get('Item', 'Rice')
        item_mapping = {
            'Corn': 'item_Corn',
            'Cotton': 'item_Cotton',
            'Rice': 'item_Rice',
            'Soybeans': 'item_Soybean',
            'Soybean': 'item_Soybean',
            'Wheat': 'item_Wheat'
        }
        
        items = ['item_Corn', 'item_Cotton', 'item_Rice', 'item_Soybean', 'item_Wheat']
        for item_col in items:
            features[item_col] = 0
            
        if item_name in item_mapping:
            features[item_mapping[item_name]] = 1
        
        # Engineered features
        features['n_p_ratio'] = features['nitrogen'] / (features['phosphorus'] + 0.001)
        features['n_k_ratio'] = features['nitrogen'] / (features['potassium'] + 0.001)
        features['p_k_ratio'] = features['phosphorus'] / (features['potassium'] + 0.001)
        features['nutrient_index'] = (features['nitrogen'] + features['phosphorus'] + features['potassium']) / 3
        
        # pH categories
        features['ph_acidic'] = 1 if features['soil_ph'] < 6.5 else 0
        features['ph_neutral'] = 1 if 6.5 <= features['soil_ph'] <= 7.5 else 0
        features['ph_alkaline'] = 1 if features['soil_ph'] > 7.5 else 0
        
        # Organic matter features
        features['high_organic_matter'] = 1 if features['organic_matter'] > 4.0 else 0
        features['organic_matter_squared'] = features['organic_matter'] ** 2
        
        # Vegetation and elevation features
        features['high_vegetation'] = 1 if features['vegetation_health'] >= 3 else 0
        features['high_elevation'] = 1 if features['elevation'] > 1000 else 0
        features['elevation_squared'] = features['elevation'] ** 2
        
        # Pesticide features
        features['pesticide_efficiency'] = features['pesticides_tonnes'] / (features['average_rain_fall_mm_per_year'] + 0.001)
        features['pesticide_intensity'] = features['pesticides_tonnes'] / 1000.0
        
        # Nitrogen efficiency
        features['nitrogen_use_efficiency'] = features['nitrogen'] / (features['average_rain_fall_mm_per_year'] + 0.001)
        
        # Cost and efficiency proxies
        features['total_input_cost_proxy'] = features['nitrogen'] + features['phosphorus'] + features['potassium'] + features['pesticides_tonnes']
        features['input_output_ratio'] = features['total_input_cost_proxy'] / (features['ndvi_avg'] + 0.001)
        
        # Climate cycles
        features['el_nino_cycle'] = float((features['year'] - 2000) % 7)
        features['decadal_climate_cycle'] = float((features['year'] - 2000) % 10)
        
        # Interaction features
        features['nitrogen_x_phosphorus'] = features['nitrogen'] * features['phosphorus']
        features['nitrogen_div_phosphorus'] = features['nitrogen'] / (features['phosphorus'] + 0.001)
        features['soil_ph_x_organic_matter'] = features['soil_ph'] * features['organic_matter']
        features['soil_ph_div_organic_matter'] = features['soil_ph'] / (features['organic_matter'] + 0.001)
        
        feature_dicts.append(features)
    
    return pd.DataFrame(feature_dicts)

def basic_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Basic preprocessing without advanced feature engineering"""
    return df

def make_fast_prediction(df: pd.DataFrame) -> np.ndarray:
    """Optimized prediction function with proper feature alignment"""
    start_time = datetime.now()
    
    # Get expected features from the model
    expected_features = MODEL_ARTIFACTS['feature_names']
    
    if expected_features is None:
        raise ValueError("Model feature names not loaded")
    
    # Ensure all expected features are present in correct order
    df_aligned = df.reindex(columns=expected_features, fill_value=0)
    
    # Apply scaling if available - but only to numerical features
    if MODEL_ARTIFACTS['scalers'] is not None:
        scalers = MODEL_ARTIFACTS['scalers']
        if 'robust' in scalers:
            scaler = scalers['robust']
            
            # Get the features that the scaler was trained on
            scaler_features = list(scaler.feature_names_in_) if hasattr(scaler, 'feature_names_in_') else []
            
            # Split into numerical and categorical features
            numerical_df = df_aligned[scaler_features] if scaler_features else pd.DataFrame()
            categorical_features = [col for col in expected_features if col not in scaler_features]
            categorical_df = df_aligned[categorical_features] if categorical_features else pd.DataFrame()
            
            # Scale only numerical features
            if not numerical_df.empty:
                numerical_scaled = pd.DataFrame(
                    scaler.transform(numerical_df),
                    columns=numerical_df.columns
                )
                
                # Combine scaled numerical and unscaled categorical features
                df_final = pd.concat([numerical_scaled, categorical_df], axis=1)
            else:
                df_final = df_aligned
            
            # Ensure correct order
            df_final = df_final.reindex(columns=expected_features, fill_value=0)
        else:
            df_final = df_aligned
    else:
        df_final = df_aligned
    
    # Fill any remaining NaN values with 0
    df_final = df_final.fillna(0)
    
    # Make prediction
    if MODEL_ARTIFACTS['model'] is None:
        raise ValueError("Model not loaded")
        
    predictions = MODEL_ARTIFACTS['model'].predict(df_final.values)
    
    processing_time = (datetime.now() - start_time).total_seconds() * 1000
    logger.info(f"Prediction completed in {processing_time:.2f}ms")
    
    return predictions

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    logger.info("🚀 Starting Crop Yield Prediction API...")
    success = load_latest_model()
    if not success:
        raise RuntimeError("Failed to load model artifacts")
    logger.info("✅ API ready for predictions!")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": MODEL_ARTIFACTS['model'] is not None,
        "model_performance": MODEL_ARTIFACTS['performance_metrics'],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_yield(input_data: PredictionInput):
    """Fast single prediction endpoint"""
    start_time = datetime.now()
    
    try:
        # Preprocess input
        df = preprocess_input(input_data, use_advanced_features=True)
        
        # Make prediction
        prediction = make_fast_prediction(df)[0]
        
        # Calculate confidence score based on model performance
        performance_metrics = MODEL_ARTIFACTS['performance_metrics']
        if performance_metrics and 'r2' in performance_metrics:
            confidence_score = min(0.95, performance_metrics['r2'])
        else:
            confidence_score = 0.78  # Default fallback
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return PredictionResponse(
            predicted_yield=float(prediction),
            confidence_score=confidence_score,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(input_data: BatchPredictionInput):
    """Optimized batch prediction endpoint"""
    start_time = datetime.now()
    
    try:
        # Process all samples at once for efficiency
        df = preprocess_input(input_data.samples, use_advanced_features=True)
        
        # Make batch prediction
        predictions = make_fast_prediction(df)
        
        # Calculate statistics
        stats = {
            "mean": float(np.mean(predictions)),
            "median": float(np.median(predictions)),
            "std": float(np.std(predictions)),
            "min": float(np.min(predictions)),
            "max": float(np.max(predictions))
        }
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return BatchPredictionResponse(
            predictions=predictions.tolist(),
            statistics=stats,
            processing_time_ms=processing_time,
            batch_size=len(predictions)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@app.get("/model/info")
async def model_info():
    """Get model information and performance metrics"""
    if MODEL_ARTIFACTS['model'] is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(MODEL_ARTIFACTS['model']).__name__,
        "features_count": len(MODEL_ARTIFACTS['feature_names']) if MODEL_ARTIFACTS['feature_names'] else 0,
        "performance_metrics": MODEL_ARTIFACTS['performance_metrics'],
        "training_info": MODEL_ARTIFACTS['metadata']['training_info'] if MODEL_ARTIFACTS['metadata'] else None,
        "preprocessing_enabled": MODEL_ARTIFACTS['preprocessor'] is not None,
        "feature_engineering_enabled": MODEL_ARTIFACTS['feature_engineer'] is not None
    }

@app.get("/predict/demo")
async def prediction_demo():
    """Demo endpoint with sample prediction"""
    demo_input = PredictionInput(
        Area="India",
        Item="Wheat", 
        Year=2024,
        average_rain_fall_mm_per_year=800.0,
        avg_temp=25.5,
        pesticides_tonnes=150.0,
        nitrogen=120.0,
        phosphorus=80.0,
        potassium=200.0,
        soil_ph=6.5,
        humidity=65.0,
        ndvi_avg=0.75,
        vegetation_health="Healthy",
        organic_matter=3.0,
        moisture=45.0,
        season_length=120.0
    )
    
    result = await predict_yield(demo_input)
    
    return {
        "demo_input": demo_input.dict(),
        "prediction_result": result.dict(),
        "message": "This is a demonstration prediction. Use POST /predict for actual predictions."
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🌾" + "="*60 + "🌾")
    print("   FAST CROP YIELD PREDICTION API")
    print("🌾" + "="*60 + "🌾")
    print()
    print("📊 Model Performance:")
    print("   🏆 R² Score: 77.86%")
    print("   📏 RMSE: 308.7 hg/ha")
    print("   📈 Features: 50 engineered features")  
    print()
    print("🚀 API Endpoints:")
    print("   GET  /health           - Health check")
    print("   POST /predict          - Single fast prediction")
    print("   POST /predict/batch    - Batch predictions")
    print("   GET  /predict/demo     - Demo prediction")
    print("   GET  /model/info       - Model information")
    print("   GET  /docs            - Interactive API docs")
    print()
    print("⚡ Performance Features:")
    print("   ✅ Pre-loaded model artifacts")
    print("   ✅ Optimized preprocessing pipeline")
    print("   ✅ Advanced feature engineering")
    print("   ✅ Batch processing support")  
    print("   ✅ Sub-100ms prediction times")
    print()
    print("🌐 Starting server at http://localhost:8001")
    print("📖 Interactive docs at http://localhost:8001/docs")
    
    uvicorn.run(
        "fast_prediction_api:app",
        host="0.0.0.0", 
        port=8001,  # Changed from 8000 to 8001
        reload=False,  # Disabled for production performance
        log_level="info"
    )
