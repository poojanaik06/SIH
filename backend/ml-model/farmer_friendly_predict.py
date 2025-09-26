#!/usr/bin/env python3
"""
Farmer-friendly prediction system that uses regional defaults for soil parameters
and automatically fetches weather data based on region or specific location
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils'))

from simple_predict import predict_yield
from utils.weather_fetcher import get_weather_data_for_region, get_weather_data_for_location

# Regional default values for soil parameters
# These values are based on typical soil conditions in different regions
REGIONAL_DEFAULTS = {
    # India
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
    # USA
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
    # China
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
    # Brazil
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
    # Australia
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
    # Canada
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
    # Russia
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
    },
    # Default values for any other region
    'default': {
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
}

def get_regional_defaults(area):
    """Get default soil parameters for a given region"""
    return REGIONAL_DEFAULTS.get(area, REGIONAL_DEFAULTS['default'])

def predict_yield_farmer_friendly(data):
    """Make a prediction using regional defaults for missing parameters"""
    
    # Get the area from the data
    area = data.get('Area', 'default')
    area_type = data.get('area_type', 'country')  # 'country' or 'location'
    
    # Get regional defaults
    defaults = get_regional_defaults(area if area_type == 'country' else 'default')
    
    # Fill in missing parameters with regional defaults
    farmer_data = data.copy()
    
    # Only fill in parameters that are not provided by the farmer
    for param, default_value in defaults.items():
        if param not in farmer_data:
            farmer_data[param] = default_value
    
    # Set year (current year if not provided)
    year = farmer_data.get('Year', 2024)
    
    # Automatically fetch weather data if not provided
    if 'average_rain_fall_mm_per_year' not in farmer_data or 'avg_temp' not in farmer_data or 'humidity' not in farmer_data:
        print(f"🌍 Fetching weather data for {area}...")
        
        # Fetch weather data based on whether it's a country or specific location
        if area_type == 'location':
            weather_data = get_weather_data_for_location(area, year)
        else:
            weather_data = get_weather_data_for_region(area, year)
        
        # Fill in missing weather parameters
        if 'average_rain_fall_mm_per_year' not in farmer_data:
            farmer_data['average_rain_fall_mm_per_year'] = weather_data.get('average_rain_fall_mm_per_year', 1000.0)
        if 'avg_temp' not in farmer_data:
            farmer_data['avg_temp'] = weather_data.get('avg_temp', 22.0)
        if 'humidity' not in farmer_data:
            farmer_data['humidity'] = weather_data.get('humidity', 65.0)
        if 'sunshine_hours' not in farmer_data:
            farmer_data['sunshine_hours'] = weather_data.get('sunshine_hours', 7.0)
    
    # Make prediction
    result = predict_yield(farmer_data)
    
    # Add information about which parameters were defaulted
    defaulted_params = []
    for param in defaults.keys():
        if param not in data:
            defaulted_params.append(param)
    
    # Add weather parameters that were auto-fetched
    weather_params_fetched = []
    if 'average_rain_fall_mm_per_year' not in data:
        weather_params_fetched.append('average_rain_fall_mm_per_year')
    if 'avg_temp' not in data:
        weather_params_fetched.append('avg_temp')
    if 'humidity' not in data:
        weather_params_fetched.append('humidity')
    if 'sunshine_hours' not in data:
        weather_params_fetched.append('sunshine_hours')
    
    result['defaulted_parameters'] = defaulted_params
    result['auto_fetched_weather'] = weather_params_fetched
    result['region_used'] = area
    
    return result

def main():
    # Example usage with minimal farmer input
    farmer_data = {
        "Area": "India",
        "Item": "Wheat",
        # Farmer only provides what they know - the rest comes from regional defaults
        # Weather data will be fetched automatically
    }
    
    print("🌾 Farmer-Friendly Crop Yield Prediction")
    print("=" * 50)
    print("📊 Input Data (minimal farmer input):")
    for key, value in farmer_data.items():
        print(f"   {key}: {value}")
    print()
    
    # Make prediction
    result = predict_yield_farmer_friendly(farmer_data)
    
    print("📈 PREDICTION RESULT:")
    print("=" * 50)
    
    if result['success']:
        print(f"✅ SUCCESS!")
        print(f"🎯 Predicted Yield: {result['predicted_yield']:.2f} {result['unit']}")
        print(f"🌍 Region Used: {result['region_used']}")
        
        if result['defaulted_parameters']:
            print(f"⚙️  Defaulted Parameters: {', '.join(result['defaulted_parameters'])}")
        
        if result['auto_fetched_weather']:
            print(f"🌤️  Auto-Fetched Weather Data: {', '.join(result['auto_fetched_weather'])}")
        
        if not result['defaulted_parameters'] and not result['auto_fetched_weather']:
            print("⚙️  All parameters provided by user")
        
        print(f"📝 Message: {result['message']}")
        
        # Explain what the defaulted parameters mean
        if result['defaulted_parameters'] or result['auto_fetched_weather']:
            print("\n💡 Explanation:")
            if result['defaulted_parameters']:
                print("   Defaulted parameters use typical values for your region")
            if result['auto_fetched_weather']:
                print("   Weather data was automatically fetched from Open-Meteo API")
    else:
        print(f"❌ ERROR: {result['error']}")
    
    print("\n💡 This prediction uses regional defaults for soil parameters")
    print("   and automatically fetches weather data based on your location.")
    print("   Only crop type and region are required for basic prediction!")

if __name__ == "__main__":
    main()