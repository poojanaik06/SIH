#!/usr/bin/env python3
"""
Simple command-line interface for farmers to predict crop yields
Automatically fetches weather data based on region or specific location
"""

import sys
import os
import warnings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils'))

# Suppress scikit-learn warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

from farmer_friendly_predict import predict_yield_farmer_friendly
from typing import Dict, Any

def get_user_input() -> Dict[str, Any]:
    """Get input from the farmer through simple prompts"""
    print("🌾 Crop Yield Prediction for Farmers")
    print("=" * 40)
    print("Answer the following questions (press Enter to use defaults):")
    print()
    
    # Ask if farmer wants to use a specific location or just country
    location_choice = input("Do you want to enter a specific location? (y/n) [n]: ").strip().lower()
    
    if location_choice == 'y' or location_choice == 'yes':
        # Get specific location
        location = input("Enter your location (e.g., 'New York, USA', 'Paris, France'): ").strip()
        if location:
            area = location
            area_type = "location"
        else:
            area = "default"
            area_type = "country"
    else:
        # Get country/region
        regions = ["India", "USA", "China", "Brazil", "Australia", "Canada", "Russia"]
        print("Available regions:")
        for i, region in enumerate(regions, 1):
            print(f"  {i}. {region}")
        
        region_choice = input(f"\nSelect your region (1-{len(regions)}) or type region name: ").strip()
        
        if region_choice.isdigit() and 1 <= int(region_choice) <= len(regions):
            area = regions[int(region_choice) - 1]
        elif region_choice in regions:
            area = region_choice
        else:
            area = "default"
            print("Using default regional values.")
        
        area_type = "country"
    
    # Get crop
    crops = ["Rice", "Wheat", "Corn", "Soybean", "Cotton"]
    print(f"\nAvailable crops:")
    for i, crop in enumerate(crops, 1):
        print(f"  {i}. {crop}")
    
    crop_choice = input(f"\nSelect your crop (1-{len(crops)}) or type crop name: ").strip()
    
    if crop_choice.isdigit() and 1 <= int(crop_choice) <= len(crops):
        item = crops[int(crop_choice) - 1]
    elif crop_choice in crops:
        item = crop_choice
    else:
        item = "Rice"  # Default crop
        print("Using Rice as default crop.")
    
    # Create basic data
    farmer_data: Dict[str, Any] = {
        "Area": area,
        "Item": item,
        "area_type": area_type  # Store whether it's a country or specific location
    }
    
    # Optional: Get year if farmer wants to predict for a specific year
    print("\nOptional information (press Enter to skip):")
    
    year_input = input("Year (e.g., 2024) [Enter for current year]: ").strip()
    if year_input:
        try:
            farmer_data["Year"] = int(year_input)
        except ValueError:
            print("Invalid year, using current year.")
    
    return farmer_data

def display_results(result: Dict[str, Any]) -> None:
    """Display prediction results in a farmer-friendly way"""
    print("\n" + "=" * 50)
    print("🌾 PREDICTION RESULTS")
    print("=" * 50)
    
    if result['success']:
        # Convert hg/ha to more familiar units
        yield_hg_ha = result['predicted_yield']
        yield_tonnes_ha = yield_hg_ha / 10000  # Convert to tonnes/hectare
        yield_bushels_acre = yield_hg_ha * 0.0143  # Approximate conversion to bushels/acre for common crops
        
        print(f"✅ SUCCESS!")
        print(f"🎯 Predicted Yield: {yield_hg_ha:.2f} hg/ha")
        print(f"                    {yield_tonnes_ha:.2f} tonnes/ha")
        print(f"                    {yield_bushels_acre:.1f} bushels/acre (approx.)")
        print()
        print(f"🌍 Region/Location: {result['region_used']}")
        print(f"🌱 Crop: {result['input_data']['Item']}")
        
        if result['defaulted_parameters'] or result.get('auto_fetched_weather', []):
            defaulted_count = len(result['defaulted_parameters'])
            weather_count = len(result.get('auto_fetched_weather', []))
            total_defaulted = defaulted_count + weather_count
            print(f"⚙️  Using defaults for {total_defaulted} parameters")
            
            if result['defaulted_parameters']:
                print("    Defaulted parameters:")
                # Group parameters by category for better understanding
                soil_params = [p for p in result['defaulted_parameters'] if p in ['soil_ph', 'nitrogen', 'phosphorus', 'potassium', 'organic_matter']]
                weather_params = [p for p in result['defaulted_parameters'] if p in ['humidity', 'sunshine_hours', 'elevation']]
                other_params = [p for p in result['defaulted_parameters'] if p not in soil_params and p not in weather_params and p not in ['ndvi_avg', 'pesticides_tonnes']]
                
                if soil_params:
                    print(f"      Soil parameters: {', '.join(soil_params)}")
                    print("        (pH, nutrients like nitrogen, phosphorus, potassium)")
                if weather_params:
                    print(f"      Weather parameters: {', '.join(weather_params)}")
                    print("        (humidity, sunshine, elevation)")
                if other_params:
                    print(f"      Other parameters: {', '.join(other_params)}")
            
            if result.get('auto_fetched_weather', []):
                print(f"    🌤️  Auto-fetched weather data: {', '.join(result['auto_fetched_weather'])}")
        else:
            print("✅ All parameters provided by user")
        
        print()
        print("💡 This prediction uses regional soil data and automatically")
        print("   fetched weather data so you don't need expensive testing equipment!")
        print("   The system used typical values for your region to fill in")
        print("   the parameters you didn't provide.")
        
        # Explain what these parameters mean
        print("\n📖 Parameter Explanations:")
        print("   • soil_ph: Acidity/alkalinity of your soil (6.0-7.5 is ideal)")
        print("   • nitrogen: Essential nutrient for leaf growth (kg/hectare)")
        print("   • phosphorus: Important for root development and flowering")
        print("   • potassium: Helps with water regulation and disease resistance")
        print("   • organic_matter: Improves soil structure and nutrient retention")
        print("   • avg_temp: Average temperature for the growing season (°C)")
        print("   • rainfall: Annual precipitation (mm/year)")
        print("   • humidity: Average relative humidity (%)")
        print("   • ndvi_avg: Vegetation health from satellite data (0.0-1.0)")
        
    else:
        print(f"❌ ERROR: {result['error']}")

def main() -> None:
    """Main function to run the farmer prediction tool"""
    try:
        # Get input from farmer
        farmer_data = get_user_input()
        
        print("\n🔄 Processing your request...")
        area_type = farmer_data.get('area_type', 'country')
        if area_type == 'location':
            print("   • Using regional defaults for soil parameters")
            print("   • Fetching weather data for your specific location...")
        else:
            print("   • Using regional defaults for soil parameters")
            print("   • Fetching weather data for your region...")
        
        # Make prediction
        result = predict_yield_farmer_friendly(farmer_data)
        
        # Display results
        display_results(result)
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using the Crop Yield Predictor!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please try again or contact support.")

if __name__ == "__main__":
    main()