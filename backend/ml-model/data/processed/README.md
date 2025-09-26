# Processed Data Directory

This directory contains cleaned and preprocessed datasets ready for model training.

## Generated Files

### 1. crop_yield_processed.csv
- Cleaned crop yield data with missing values handled
- Feature-engineered columns added
- Outliers removed or capped

### 2. weather_processed.csv
- Weather data with derived features (temperature range, heat index)
- Aggregated daily/monthly statistics
- Missing weather data interpolated

### 3. soil_processed.csv
- Standardized soil measurements
- Categorical soil types encoded
- Soil quality indices calculated

### 4. ndvi_processed.csv
- NDVI data with statistical features (mean, max, min)
- Temporal aggregations
- Vegetation indices derived

### 5. integrated_dataset.csv
- Final merged dataset combining all data sources
- Ready for machine learning model training
- Features selected and engineered

## Processing Steps Applied
1. Data cleaning and missing value imputation
2. Outlier detection and treatment
3. Feature engineering and creation
4. Data normalization and standardization
5. Categorical encoding
6. Data integration and merging

## Usage
Load these processed files directly into model training notebooks.