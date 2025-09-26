# Sample Raw Data Files
# Place your actual datasets in this directory

## Expected Data Structure

### 1. crop_yield_data.csv
- Columns: location, date, crop_type, yield, area_harvested, production
- Description: Historical crop yield data

### 2. weather_data.csv  
- Columns: location, date, temperature_max, temperature_min, rainfall, humidity, sunshine_hours
- Description: Weather data for different locations and dates

### 3. soil_data.csv
- Columns: location, soil_ph, nitrogen, phosphorus, potassium, organic_matter, soil_type
- Description: Soil characteristics by location

### 4. ndvi_data.csv
- Columns: location, date, ndvi_value, satellite_source
- Description: NDVI (Normalized Difference Vegetation Index) data from satellite imagery

## Data Sources
- Weather data: National weather services, APIs like OpenWeatherMap
- Soil data: Agricultural surveys, government databases
- NDVI data: Google Earth Engine, Sentinel-2, Landsat
- Crop yield: Agricultural statistics, FAO databases

## File Formats
- CSV format recommended
- UTF-8 encoding
- Date format: YYYY-MM-DD
- Numeric values: decimal notation