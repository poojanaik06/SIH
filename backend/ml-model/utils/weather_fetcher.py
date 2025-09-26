#!/usr/bin/env python3
"""
Weather data fetcher for agricultural applications
Fetches real-time and historical weather data from Open-Meteo API
Supports both country-level and specific location-level weather data
"""

import requests
import json
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
from geopy.geocoders import Nominatim
import time

# Open-Meteo API endpoints
WEATHER_API_BASE = "https://archive-api.open-meteo.com/v1/archive"

def get_country_coordinates(country: str) -> Dict[str, float]:
    """
    Get approximate coordinates for major agricultural regions
    These are center points for countries/regions
    """
    coordinates = {
        'India': {'latitude': 20.5937, 'longitude': 78.9629},
        'USA': {'latitude': 37.0902, 'longitude': -95.7129},
        'China': {'latitude': 35.8617, 'longitude': 104.1954},
        'Brazil': {'latitude': -14.2350, 'longitude': -51.9253},
        'Australia': {'latitude': -25.2744, 'longitude': 133.7751},
        'Canada': {'latitude': 56.1304, 'longitude': -106.3468},
        'Russia': {'latitude': 61.5240, 'longitude': 105.3188},
        'default': {'latitude': 20.0, 'longitude': 0.0}
    }
    
    return coordinates.get(country, coordinates['default'])

def geocode_location(location: str) -> Optional[Tuple[float, float]]:
    """
    Convert a location string to latitude and longitude coordinates
    
    Args:
        location: Location string (e.g., "New York, USA", "Paris, France")
    
    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    try:
        # Initialize geocoder with a user agent
        geolocator = Nominatim(user_agent="crop_yield_predictor")
        
        # Geocode the location
        location_obj = geolocator.geocode(location)
        
        if location_obj:
            return (location_obj.latitude, location_obj.longitude)
        else:
            return None
            
    except Exception as e:
        print(f"Error geocoding location '{location}': {e}")
        return None

def fetch_historical_weather_data(
    latitude: float, 
    longitude: float, 
    start_date: str, 
    end_date: str
) -> Optional[Dict[str, Any]]:
    """
    Fetch historical weather data from Open-Meteo API
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dictionary with weather data or None if error
    """
    try:
        # Construct API URL
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date,
            'end_date': end_date,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,sunshine_duration',
            'timezone': 'auto'
        }
        
        # Make request
        response = requests.get(WEATHER_API_BASE, params=params)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing weather data: {e}")
        return None

def calculate_average_weather_metrics(weather_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate average weather metrics from historical data
    
    Args:
        weather_data: Raw weather data from API
    
    Returns:
        Dictionary with averaged weather metrics
    """
    if not weather_data or 'daily' not in weather_data:
        return {}
    
    daily_data = weather_data['daily']
    
    # Calculate averages with better error handling
    temp_max_list = daily_data.get('temperature_2m_max', [])
    temp_min_list = daily_data.get('temperature_2m_min', [])
    precipitation_list = daily_data.get('precipitation_sum', [])
    rain_list = daily_data.get('rain_sum', [])
    sunshine_list = daily_data.get('sunshine_duration', [])
    
    # Calculate averages
    avg_max_temp = sum(temp_max_list) / len(temp_max_list) if temp_max_list and len(temp_max_list) > 0 else 0
    avg_min_temp = sum(temp_min_list) / len(temp_min_list) if temp_min_list and len(temp_min_list) > 0 else 0
    avg_precipitation = sum(precipitation_list) / len(precipitation_list) if precipitation_list and len(precipitation_list) > 0 else 0
    avg_rain = sum(rain_list) / len(rain_list) if rain_list and len(rain_list) > 0 else 0
    
    # Calculate average temperature
    avg_temp = (avg_max_temp + avg_min_temp) / 2 if avg_max_temp != 0 and avg_min_temp != 0 else 22.0
    
    # Calculate approximate humidity (this is a rough estimation)
    # In reality, humidity would come from a different API endpoint
    # For now, we'll use a simple estimation based on temperature and precipitation
    humidity_estimate = min(100, max(30, 70 - (avg_temp - 15) * 2 + avg_precipitation * 0.5))
    
    # Calculate sunshine hours from sunshine duration (convert from seconds to hours)
    avg_sunshine_seconds = sum(sunshine_list) / len(sunshine_list) if sunshine_list and len(sunshine_list) > 0 else 0
    avg_sunshine_hours = avg_sunshine_seconds / 3600  # Convert seconds to hours
    
    # Convert precipitation from mm over the period to annual mm
    # This is a rough approximation - in reality, we'd fetch a full year of data
    days_of_data = len(rain_list) if rain_list else 0
    annual_rainfall_estimate = (avg_rain * 365) if days_of_data > 0 else 1000.0
    
    return {
        'avg_temp': round(avg_temp, 1),
        'average_rain_fall_mm_per_year': round(annual_rainfall_estimate, 1),
        'humidity': round(humidity_estimate, 1),
        'sunshine_hours': round(avg_sunshine_hours, 1)
    }

def get_weather_data_for_region(area: str, year: Optional[int] = None) -> Dict[str, float]:
    """
    Get weather data for a specific region and year
    
    Args:
        area: Country/region name
        year: Year for historical data (current year if None)
    
    Returns:
        Dictionary with weather metrics
    """
    # Get coordinates for the area
    coords = get_country_coordinates(area)
    
    # Use current year or specified year
    if year is None:
        year = datetime.now().year
    
    # For historical data, we'll fetch the previous year's data as it's more likely to be complete
    target_year = year - 1 if year > 2020 else 2020
    
    # Define date range (we'll fetch a representative period)
    start_date = f"{target_year}-01-01"
    end_date = f"{target_year}-12-31"
    
    # Fetch weather data
    weather_data = fetch_historical_weather_data(
        coords['latitude'], 
        coords['longitude'], 
        start_date, 
        end_date
    )
    
    if weather_data:
        # Calculate average metrics
        avg_metrics = calculate_average_weather_metrics(weather_data)
        return avg_metrics
    else:
        # Return default values if API fails
        print(f"⚠️  Could not fetch weather data for {area}. Using default values.")
        return {
            'avg_temp': 22.0,
            'average_rain_fall_mm_per_year': 1000.0,
            'humidity': 65.0,
            'sunshine_hours': 7.0
        }

def get_weather_data_for_location(location: str, year: Optional[int] = None) -> Dict[str, float]:
    """
    Get weather data for a specific location and year
    
    Args:
        location: Specific location (e.g., "New York, USA", "Paris, France")
        year: Year for historical data (current year if None)
    
    Returns:
        Dictionary with weather metrics
    """
    # Geocode the location to get coordinates
    print(f"🌍 Geocoding location: {location}")
    coords = geocode_location(location)
    
    if not coords:
        print(f"⚠️  Could not geocode location '{location}'. Using default values.")
        return {
            'avg_temp': 22.0,
            'average_rain_fall_mm_per_year': 1000.0,
            'humidity': 65.0,
            'sunshine_hours': 7.0
        }
    
    latitude, longitude = coords
    print(f"📍 Found coordinates: {latitude}, {longitude}")
    
    # Use current year or specified year
    if year is None:
        year = datetime.now().year
    
    # For historical data, we'll fetch the previous year's data as it's more likely to be complete
    target_year = year - 1 if year > 2020 else 2020
    
    # Define date range (we'll fetch a representative period)
    start_date = f"{target_year}-01-01"
    end_date = f"{target_year}-12-31"
    
    # Fetch weather data
    weather_data = fetch_historical_weather_data(
        latitude, 
        longitude, 
        start_date, 
        end_date
    )
    
    if weather_data:
        # Calculate average metrics
        avg_metrics = calculate_average_weather_metrics(weather_data)
        return avg_metrics
    else:
        # Return default values if API fails
        print(f"⚠️  Could not fetch weather data for {location}. Using default values.")
        return {
            'avg_temp': 22.0,
            'average_rain_fall_mm_per_year': 1000.0,
            'humidity': 65.0,
            'sunshine_hours': 7.0
        }

def main():
    """Example usage"""
    print("🌤️  Weather Data Fetcher Example")
    print("=" * 40)
    
    # Test with different regions
    test_regions = ['India', 'USA', 'Brazil']
    
    for region in test_regions:
        print(f"\n📍 {region}:")
        weather = get_weather_data_for_region(region)
        for key, value in weather.items():
            print(f"  {key}: {value}")
    
    # Test with specific locations
    print("\n" + "=" * 40)
    print("📍 Location-based weather data:")
    
    test_locations = ['New York, USA', 'London, UK', 'Tokyo, Japan']
    
    for location in test_locations:
        print(f"\n📍 {location}:")
        weather = get_weather_data_for_location(location)
        for key, value in weather.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()