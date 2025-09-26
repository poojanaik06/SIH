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
    # For specific locations, try to map to country first
    area_lower = area.lower()
    
    # Map specific locations to countries
    location_to_country = {
        'mangalore': 'India',
        'bangalore': 'India', 
        'mumbai': 'India',
        'delhi': 'India',
        'kolkata': 'India',
        'chennai': 'India',
        'hyderabad': 'India',
        'pune': 'India',
        'goa': 'India',
        'kerala': 'India',
        'karnataka': 'India',
        'gujarat': 'India',
        'maharashtra': 'India',
        'punjab': 'India',
        'haryana': 'India',
        'uttar pradesh': 'India',
        'rajasthan': 'India',
        'bihar': 'India',
        'west bengal': 'India',
        'assam': 'India',
        'odisha': 'India',
        'california': 'USA',
        'texas': 'USA',
        'florida': 'USA',
        'new york': 'USA',
        'iowa': 'USA',
        'illinois': 'USA',
        'kansas': 'USA',
        'nebraska': 'USA',
        'beijing': 'China',
        'shanghai': 'China',
        'guangzhou': 'China',
        'sao paulo': 'Brazil',
        'rio de janeiro': 'Brazil',
        'sydney': 'Australia',
        'melbourne': 'Australia',
        'toronto': 'Canada',
        'vancouver': 'Canada',
        'moscow': 'Russia',
        'paris': 'default',  # No specific data for France, use default
        'london': 'default',  # No specific data for UK, use default
    }
    
    # Check if it's a specific location we can map
    for location, country in location_to_country.items():
        if location in area_lower:
            return REGIONAL_DEFAULTS.get(country, REGIONAL_DEFAULTS['default'])
    
    # Check if it's directly a country in our defaults
    for country in REGIONAL_DEFAULTS.keys():
        if country.lower() in area_lower:
            return REGIONAL_DEFAULTS[country]
    
    # If no match found, return defaults
    return REGIONAL_DEFAULTS['default']

def predict_yield_farmer_friendly(data):
    """Make a prediction using regional defaults and real weather data for more accurate results"""
    
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
    
    # Always fetch weather data to get location-specific conditions
    print(f"🌍 Fetching weather data for {area}...")
    
    # Fetch weather data based on whether it's a country or specific location
    if area_type == 'location':
        weather_data = get_weather_data_for_location(area, year)
    else:
        weather_data = get_weather_data_for_region(area, year)
    
    # Use real weather data with fallbacks
    farmer_data['average_rain_fall_mm_per_year'] = weather_data.get('average_rain_fall_mm_per_year', 1000.0)
    farmer_data['avg_temp'] = weather_data.get('avg_temp', 22.0)
    farmer_data['humidity'] = weather_data.get('humidity', 65.0)
    farmer_data['sunshine_hours'] = weather_data.get('sunshine_hours', 7.0)
    
    # Apply location-specific climate adjustments to soil parameters
    farmer_data = apply_climate_soil_adjustments(farmer_data, weather_data, area)
    
    # Track which parameters were defaulted vs fetched
    defaulted_params = []
    auto_fetched_weather = ['average_rain_fall_mm_per_year', 'avg_temp', 'humidity', 'sunshine_hours']
    
    # Check what was defaulted from user input
    for param in defaults.keys():
        if param not in data and param not in auto_fetched_weather:
            defaulted_params.append(param)
    
    # Make prediction
    result = predict_yield(farmer_data)
    
    result['defaulted_parameters'] = defaulted_params
    result['auto_fetched_weather'] = auto_fetched_weather
    result['region_used'] = area
    result['weather_conditions'] = {
        'temperature': weather_data.get('avg_temp', 22.0),
        'rainfall': weather_data.get('average_rain_fall_mm_per_year', 1000.0),
        'humidity': weather_data.get('humidity', 65.0),
        'sunshine_hours': weather_data.get('sunshine_hours', 7.0)
    }
    
    return result

def apply_climate_soil_adjustments(farmer_data, weather_data, location):
    """Apply climate-based adjustments to soil parameters for more realistic predictions"""
    
    temp = weather_data.get('avg_temp', 22.0)
    rainfall = weather_data.get('average_rain_fall_mm_per_year', 1000.0)
    humidity = weather_data.get('humidity', 65.0)
    
    # Temperature-based soil adjustments
    if temp > 35:  # Very hot climate
        farmer_data['soil_ph'] = max(farmer_data.get('soil_ph', 6.5) - 0.2, 5.5)  # Slightly more acidic
        farmer_data['organic_matter'] = max(farmer_data.get('organic_matter', 2.0) - 0.3, 0.5)  # Lower organic matter
        farmer_data['nitrogen'] = farmer_data.get('nitrogen', 150) * 0.9  # Reduced nitrogen retention
    elif temp < 10:  # Very cold climate
        farmer_data['soil_ph'] = min(farmer_data.get('soil_ph', 6.5) + 0.1, 8.0)  # Slightly more alkaline
        farmer_data['organic_matter'] = farmer_data.get('organic_matter', 2.0) * 1.2  # Higher organic matter
        farmer_data['nitrogen'] = farmer_data.get('nitrogen', 150) * 1.1  # Better nitrogen retention
    
    # Rainfall-based soil adjustments
    if rainfall > 2000:  # High rainfall areas
        farmer_data['soil_ph'] = max(farmer_data.get('soil_ph', 6.5) - 0.3, 5.0)  # More acidic (leaching)
        farmer_data['potassium'] = farmer_data.get('potassium', 150) * 0.8  # Potassium leaching
        farmer_data['phosphorus'] = farmer_data.get('phosphorus', 30) * 0.9  # Phosphorus leaching
    elif rainfall < 500:  # Arid/semi-arid areas
        farmer_data['soil_ph'] = min(farmer_data.get('soil_ph', 6.5) + 0.3, 8.5)  # More alkaline
        farmer_data['organic_matter'] = max(farmer_data.get('organic_matter', 2.0) - 0.5, 0.2)  # Lower organic matter
        farmer_data['nitrogen'] = farmer_data.get('nitrogen', 150) * 0.7  # Lower nitrogen
    
    # Humidity-based adjustments
    if humidity > 80:  # Very humid
        farmer_data['ndvi_avg'] = min(farmer_data.get('ndvi_avg', 0.65) + 0.05, 0.9)  # Better vegetation
    elif humidity < 40:  # Very dry
        farmer_data['ndvi_avg'] = max(farmer_data.get('ndvi_avg', 0.65) - 0.1, 0.3)  # Stressed vegetation
    
    # Location-specific soil type adjustments
    location_lower = location.lower()
    
    # Coastal areas (higher salinity)
    if any(word in location_lower for word in ['mumbai', 'chennai', 'kolkata', 'goa', 'cochin', 'coastal']):
        farmer_data['soil_ph'] = min(farmer_data.get('soil_ph', 6.5) + 0.2, 8.0)
        farmer_data['potassium'] = farmer_data.get('potassium', 150) * 1.1  # Higher potassium in coastal soils
    
    # Hill stations and mountainous areas
    if any(word in location_lower for word in ['ooty', 'shimla', 'darjeeling', 'hill', 'mountain']):
        farmer_data['elevation'] = 1500.0  # Higher elevation
        farmer_data['organic_matter'] = farmer_data.get('organic_matter', 2.0) * 1.3
        farmer_data['soil_ph'] = max(farmer_data.get('soil_ph', 6.5) - 0.1, 5.8)
    
    # Desert/arid regions
    if any(word in location_lower for word in ['rajasthan', 'jodhpur', 'bikaner', 'desert', 'arid']):
        farmer_data['soil_ph'] = min(farmer_data.get('soil_ph', 6.5) + 0.5, 8.5)
        farmer_data['organic_matter'] = max(farmer_data.get('organic_matter', 2.0) - 0.8, 0.1)
        farmer_data['nitrogen'] = farmer_data.get('nitrogen', 150) * 0.6
    
    # Fertile plains (Gangetic plains, etc.)
    if any(word in location_lower for word in ['punjab', 'haryana', 'uttar pradesh', 'bihar', 'gangetic']):
        farmer_data['nitrogen'] = farmer_data.get('nitrogen', 150) * 1.2
        farmer_data['phosphorus'] = farmer_data.get('phosphorus', 30) * 1.1
        farmer_data['organic_matter'] = farmer_data.get('organic_matter', 2.0) * 1.1
    
    return farmer_data

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