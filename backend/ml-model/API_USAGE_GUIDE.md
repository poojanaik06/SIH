# Crop Yield Prediction API Usage Guide

## Starting the API Server

1. Navigate to the deployment directory:
   ```
   cd d:\ml-model\deployment
   ```

2. Start the FastAPI server:
   ```
   python fast_prediction_api.py
   ```

3. The server will start on port 8001:
   - Health check: http://localhost:8001/health
   - Prediction endpoint: http://localhost:8001/predict
   - API documentation: http://localhost:8001/docs

## API Endpoints

### 1. Health Check
**GET** `/health`
- Returns the health status of the API and model loading status

### 2. Single Prediction
**POST** `/predict`
- Accepts crop data and returns yield prediction

### 3. Batch Prediction
**POST** `/predict/batch`
- Accepts multiple crop data samples and returns batch predictions

### 4. Demo Prediction
**GET** `/predict/demo`
- Returns a sample prediction with demo data

### 5. Model Information
**GET** `/model/info`
- Returns information about the loaded model and its performance metrics

## Making Predictions

### Required Fields
- `Area`: Geographic area/country (string)
- `Item`: Crop type (string)
- `Year`: Year (integer, 2000-2030)
- `average_rain_fall_mm_per_year`: Annual rainfall in mm (float)
- `avg_temp`: Average temperature in Celsius (float)
- `pesticides_tonnes`: Pesticides used in tonnes (float)

### Optional Fields
- `nitrogen`: Nitrogen content (float)
- `phosphorus`: Phosphorus content (float)
- `potassium`: Potassium content (float)
- `soil_ph`: Soil pH level (float)
- `humidity`: Humidity percentage (float)
- `ndvi_avg`: NDVI average (float)
- `vegetation_health`: Vegetation health status (string: "Poor", "Fair", "Good", "Healthy")
- `organic_matter`: Organic matter content (float)
- `moisture`: Soil moisture (float)
- `season_length`: Growing season length (float)

### Example Request

```json
{
  "Area": "India",
  "Item": "Rice",
  "Year": 2023,
  "average_rain_fall_mm_per_year": 1200.0,
  "avg_temp": 25.5,
  "pesticides_tonnes": 100.0,
  "nitrogen": 80.0,
  "phosphorus": 40.0,
  "potassium": 60.0,
  "soil_ph": 6.5,
  "humidity": 65.0,
  "ndvi_avg": 0.75,
  "vegetation_health": "Healthy",
  "organic_matter": 3.0
}
```

### Example Response

```json
{
  "predicted_yield": 3976.10,
  "unit": "hg/ha",
  "confidence_score": 0.7786,
  "processing_time_ms": 2.5
}
```

## Using the API with Python

```python
import requests
import json

# Test data
test_data = {
    "Area": "India",
    "Item": "Rice",
    "Year": 2023,
    "average_rain_fall_mm_per_year": 1200.0,
    "avg_temp": 25.5,
    "pesticides_tonnes": 100.0,
    "nitrogen": 80.0,
    "phosphorus": 40.0,
    "potassium": 60.0,
    "soil_ph": 6.5,
    "humidity": 65.0,
    "ndvi_avg": 0.75,
    "vegetation_health": "Healthy",
    "organic_matter": 3.0
}

# Make prediction request
response = requests.post(
    "http://localhost:8001/predict",
    headers={"Content-Type": "application/json"},
    data=json.dumps(test_data)
)

print("Status Code:", response.status_code)
print("Response:", response.json())
```

## Using the API with cURL (Windows PowerShell)

```powershell
# Note: PowerShell's curl alias maps to Invoke-WebRequest which has different syntax
# Use the full path to curl or use Invoke-WebRequest directly

# Using Invoke-WebRequest
Invoke-WebRequest -Uri "http://localhost:8001/predict" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"Area": "India", "Item": "Rice", "Year": 2023, "average_rain_fall_mm_per_year": 1200.0, "avg_temp": 25.5, "pesticides_tonnes": 100.0, "nitrogen": 80.0, "phosphorus": 40.0, "potassium": 60.0, "soil_ph": 6.5, "humidity": 65.0, "ndvi_avg": 0.75, "vegetation_health": "Healthy", "organic_matter": 3.0}'
```

## Troubleshooting

### Common Issues

1. **Port already in use**: If you get an error about port 8001 being in use, change the port in `fast_prediction_api.py`:
   ```python
   uvicorn.run(
       "fast_prediction_api:app",
       host="0.0.0.0", 
       port=8002,  # Change to another available port
       reload=False,
       log_level="info"
   )
   ```

2. **Model loading errors**: Ensure all model files are in the `models` directory:
   - `random_forest_crop_yield_20250925_224814.joblib`
   - `random_forest_crop_yield_20250925_224814_features.joblib`
   - `random_forest_crop_yield_20250925_224814_scalers.joblib`
   - `random_forest_crop_yield_20250925_224814_metadata.json`

3. **Feature mismatch errors**: Make sure all required fields are provided in the request and that categorical values match expected values.

### Expected Areas
- Argentina
- Australia
- Brazil
- Canada
- China
- France
- Germany
- India
- Italy
- Japan
- Mexico
- Russian Federation
- Spain
- Turkey
- Ukraine
- United Kingdom
- United States of America

### Expected Items
- Barley
- Cassava
- Corn
- Cotton
- Potatoes
- Rice
- Soybeans
- Sugar beet
- Sugarcane
- Sweet potatoes
- Wheat

## Performance

The API is optimized for fast predictions:
- Sub-100ms prediction times
- Pre-loaded model artifacts
- Optimized preprocessing pipeline
- Batch processing support for multiple samples