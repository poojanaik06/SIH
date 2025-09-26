# ML Model for Crop Yield Prediction 🌾

This directory contains the complete machine learning pipeline for predicting crop yields based on soil characteristics, weather data, and NDVI (satellite imagery) data.

## 📁 Directory Structure

```
ml-model/
│
├── notebooks/                     # 📓 Jupyter Notebooks
│   ├── 01_data_preprocessing.ipynb    # Data cleaning and preprocessing
│   ├── 02_model_training.ipynb        # Model training and comparison
│   └── 03_model_evaluation.ipynb      # Model evaluation and analysis
│
├── data/                          # 📊 Data Storage
│   ├── raw/                          # Raw datasets (CSV from Kaggle, GEE)
│   └── processed/                    # Cleaned and preprocessed datasets
│
├── models/                        # 🤖 Trained Models
│   ├── xgb_crop_yield_model.joblib    # Main XGBoost model
│   ├── feature_scaler.joblib          # Feature scaling object
│   ├── label_encoders.joblib          # Categorical encoders
│   ├── feature_names.joblib           # Feature names list
│   └── model_metadata.joblib          # Model metadata and metrics
│
├── utils/                         # 🛠 Utility Scripts
│   ├── __init__.py                    # Package initialization
│   ├── preprocessing.py               # Data preprocessing utilities
│   ├── feature_engineering.py        # Feature engineering utilities
│   └── weather_fetcher.py            # Automatic weather data fetching with geolocation
│
├── examples/                      # 🌱 Farmer-Friendly Examples
│   └── farmer_examples.py             # Examples for different input levels
│
├── train.py                       # 🚀 Main training script
├── config.yml                     # ⚙️ Configuration file
├── requirements.txt              # 📦 Python dependencies
├── farmers_predict.py            # 🚜 Simple farmer interface with location support
├── farmer_friendly_predict.py    # 🌾 Regional defaults predictor with location support
└── README.md                     # 📖 This file
```

## 🎯 Model Overview

The crop yield prediction model uses:

- **Input Features**: Soil properties (pH, nutrients), weather data (temperature, rainfall, humidity), NDVI vegetation indices, geographic location
- **Target Variable**: Crop yield (tons per hectare)
- **Model Types**: XGBoost (primary), Random Forest, Linear Regression
- **Performance**: R² > 0.8, RMSE < 5 tons/ha (typical performance)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data

Place your raw datasets in the `data/raw/` directory:
- `crop_yield_data.csv` - Historical yield data
- `weather_data.csv` - Weather station data
- `soil_data.csv` - Soil analysis data
- `ndvi_data.csv` - Satellite NDVI data

### 3. Run Data Preprocessing

```bash
# Using Jupyter notebooks (recommended for exploration)
jupyter notebook notebooks/01_data_preprocessing.ipynb

# Or use the training script directly
python train.py --config config.yml
```

### 4. Train the Model

```bash
# Train with default XGBoost model
python train.py

# Train with specific model type
python train.py --model_type random_forest

# Train with custom configuration
python train.py --config custom_config.yml
```

### 5. Farmer-Friendly Prediction

For farmers who don't have detailed soil testing equipment, we provide several simplified interfaces:

```bash
# Interactive command-line interface for farmers (recommended)
python farmers_predict.py

# Programmatic interface with regional defaults
python farmer_friendly_predict.py

# Examples showing different input levels
python examples/farmer_examples.py
```

The farmer-friendly system automatically uses regional default values for soil parameters and **fetches real weather data** based on:
- **Country/Region level**: Select from predefined countries
- **Specific Location level**: Enter specific locations like "Karnataka, India" or "California, USA"

Farmers only need to provide:
- Location (country/region or specific location)
- Crop type
- Optional: Year for prediction

## 📊 Data Requirements

### Input Data Format

Your raw data should include the following columns:

#### Crop Yield Data (`crop_yield_data.csv`)
- `location` - Farm/field identifier
- `date` - Harvest date (YYYY-MM-DD)
- `crop_type` - Type of crop (wheat, rice, corn, etc.)
- `yield` - Crop yield in tons per hectare
- `area_harvested` - Area harvested in hectares

#### Weather Data (`weather_data.csv`)
- `location` - Location identifier
- `date` - Date (YYYY-MM-DD)
- `temperature_max` - Maximum temperature (°C)
- `temperature_min` - Minimum temperature (°C)
- `rainfall` - Daily rainfall (mm)
- `humidity` - Relative humidity (%)
- `sunshine_hours` - Daily sunshine hours

#### Soil Data (`soil_data.csv`)
- `location` - Location identifier
- `soil_ph` - Soil pH (6.0-8.0)
- `nitrogen` - Nitrogen content (mg/kg)
- `phosphorus` - Phosphorus content (mg/kg)
- `potassium` - Potassium content (mg/kg)
- `organic_matter` - Organic matter percentage (%)

#### NDVI Data (`ndvi_data.csv`)
- `location` - Location identifier
- `date` - Date (YYYY-MM-DD)
- `ndvi_value` - NDVI value (0.0-1.0)
- `satellite_source` - Data source (Sentinel-2, Landsat, etc.)

## ⚙️ Configuration

The model behavior is controlled through `config.yml`. Key sections:

### Data Configuration
```yaml
data:
  processed_data_path: "data/processed/"
  target_column: "yield"
  test_size: 0.2
```

### Model Configuration
```yaml
model:
  type: "xgboost"  # xgboost, random_forest, linear, ridge
  hyperparameter_tuning: true
  cv_folds: 5
```

### Feature Engineering
```yaml
feature_engineering:
  create_interactions: true
  create_polynomials: false
  create_temporal_features: true
```

## 🛠 Utility Functions

### Data Preprocessing (`utils/preprocessing.py`)
- `DataPreprocessor` - Main preprocessing class
- `handle_missing_values()` - Handle missing data
- `remove_outliers()` - Outlier detection and removal
- `encode_categorical_variables()` - Categorical encoding
- `scale_features()` - Feature scaling

### Feature Engineering (`utils/feature_engineering.py`)
- `FeatureEngineer` - Main feature engineering class
- `create_weather_features()` - Weather-derived features
- `create_soil_features()` - Soil-derived features
- `create_ndvi_features()` - Vegetation indices
- `create_interaction_features()` - Feature interactions

### Weather Data Fetching (`utils/weather_fetcher.py`)
- `get_weather_data_for_region()` - Automatically fetch weather data by country/region
- `get_weather_data_for_location()` - Automatically fetch weather data by specific location
- `get_country_coordinates()` - Get coordinates for regions
- `geocode_location()` - Convert location strings to coordinates
- `fetch_historical_weather_data()` - Fetch data from Open-Meteo API

## 📈 Model Performance

### Evaluation Metrics
- **R² Score**: Coefficient of determination (target: > 0.8)
- **RMSE**: Root Mean Square Error (target: < 5 tons/ha)
- **MAE**: Mean Absolute Error (target: < 3 tons/ha)
- **MAPE**: Mean Absolute Percentage Error (target: < 15%)

### Cross-Validation
- 5-fold cross-validation for robust performance estimation
- Stratified sampling to maintain data distribution

## 🔬 Model Interpretability

### Feature Importance
- Built-in feature importance for tree-based models
- Correlation analysis for linear models
- SHAP values for detailed explanations (optional)

### Key Features (Typical)
1. **NDVI Average** - Vegetation health indicator
2. **Rainfall** - Water availability
3. **Nitrogen Content** - Soil fertility
4. **Average Temperature** - Growing conditions
5. **Soil pH** - Nutrient availability

## 🌱 Farmer-Friendly Features

### Regional Default Values

The system includes regional default values for soil parameters, eliminating the need for expensive soil testing:

- **India**: pH 7.0, Nitrogen 250 kg/ha, etc.
- **USA**: pH 6.5, Nitrogen 150 kg/ha, etc.
- **China**: pH 7.5, Nitrogen 200 kg/ha, etc.
- **Brazil**: pH 5.5, Nitrogen 120 kg/ha, etc.
- **Australia**: pH 7.2, Nitrogen 100 kg/ha, etc.
- **Canada**: pH 6.8, Nitrogen 180 kg/ha, etc.
- **Russia**: pH 6.0, Nitrogen 90 kg/ha, etc.

### Location-Based Weather Data Fetching

The system automatically fetches real weather data from the Open-Meteo API:

#### Country/Region Level
- Select from predefined countries/regions
- Uses center coordinates of the country
- Fetches representative weather data

#### Specific Location Level
- Enter specific locations like "Karnataka, India" or "California, USA"
- Uses geocoding to get exact coordinates
- Fetches weather data specific to your location
- More accurate than country-level data

Weather parameters automatically fetched:
- **Temperature**: Average growing season temperatures
- **Rainfall**: Annual precipitation data
- **Humidity**: Regional humidity patterns
- **Sunshine**: Daily sunshine hours

### Progressive Input System

Farmers can provide information at different levels:
1. **Minimal**: Only location and crop type (system uses all defaults + real weather data)
2. **Basic**: Add specific year for prediction
3. **Detailed**: Provide soil test results if available (maximum accuracy)

### Simple Interface

The `farmers_predict.py` script provides a simple command-line interface that guides farmers through the process with clear questions and explanations.

## 🚀 Production Deployment

### Model Artifacts
The trained model produces:
- `xgb_crop_yield_model.joblib` - Trained model
- `feature_scaler.joblib` - Preprocessing scaler
- `label_encoders.joblib` - Categorical encoders
- `feature_names.joblib` - Expected feature names
- `model_metadata.joblib` - Model metadata

### Making Predictions
```python
import joblib
import pandas as pd

# Load model artifacts
model = joblib.load('models/xgb_crop_yield_model.joblib')
scaler = joblib.load('models/feature_scaler.joblib')
encoders = joblib.load('models/label_encoders.joblib')
feature_names = joblib.load('models/feature_names.joblib')

# Prepare new data
new_data = pd.DataFrame({...})  # Your input data
# Apply same preprocessing as training data
# Make prediction
yield_prediction = model.predict(new_data)
```

## 📋 Requirements

See `requirements.txt` for complete dependencies. Key packages:
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning
- `xgboost` - Gradient boosting
- `matplotlib` & `seaborn` - Visualization
- `jupyter` - Notebook environment

## 🐛 Troubleshooting

### Common Issues

1. **Memory Errors**
   - Reduce dataset size or batch processing
   - Adjust `n_jobs` parameter in config

2. **Missing Data Errors**
   - Check data format and column names
   - Verify date formats (YYYY-MM-DD)

3. **Low Model Performance**
   - Check data quality and outliers
   - Consider feature engineering
   - Increase model complexity

4. **Slow Training**
   - Reduce hyperparameter search space
   - Use smaller CV folds
   - Enable GPU acceleration (if available)

## 📝 Logging

Training logs are saved to `logs/training.log` with:
- Data loading and preprocessing steps
- Model training progress
- Performance metrics
- Error messages and warnings

## 🤝 Contributing

To extend the model:

1. Add new feature engineering functions to `utils/feature_engineering.py`
2. Implement new preprocessing steps in `utils/preprocessing.py`
3. Add new model types to `train.py`
4. Update configuration in `config.yml`
5. Create evaluation notebooks for new features

## 📄 License

This ML model is part of the AI Crop Yield Prediction system. See main project LICENSE for details.

## 📞 Support

For technical support:
- Check logs in `logs/training.log`
- Review configuration in `config.yml`
- Run data validation notebooks
- Check data format requirements

---

**Happy Modeling! 🌾🤖**