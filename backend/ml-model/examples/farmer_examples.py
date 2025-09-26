#!/usr/bin/env python3
"""
Examples showing how farmers can use the prediction system with different levels of input
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from farmer_friendly_predict import predict_yield_farmer_friendly

def example_1_minimal_input():
    """Example 1: Minimal input - only region and crop"""
    print("🌾 Example 1: Minimal Input")
    print("=" * 40)
    
    farmer_data = {
        "Area": "India",
        "Item": "Rice"
    }
    
    print("Input provided by farmer:")
    for key, value in farmer_data.items():
        print(f"  {key}: {value}")
    
    result = predict_yield_farmer_friendly(farmer_data)
    
    if result['success']:
        print(f"\n🎯 Predicted Yield: {result['predicted_yield']:.2f} {result['unit']}")
        print(f"🌍 Region Used: {result['region_used']}")
        print(f"⚙️  Number of defaulted parameters: {len(result['defaulted_parameters'])}")
    else:
        print(f"❌ Error: {result['error']}")

def example_2_basic_input():
    """Example 2: Basic input - region, crop, and some weather info"""
    print("\n\n🌾 Example 2: Basic Input")
    print("=" * 40)
    
    farmer_data = {
        "Area": "USA",
        "Item": "Corn",
        "Year": 2024,
        "average_rain_fall_mm_per_year": 900.0,
        "avg_temp": 24.0
    }
    
    print("Input provided by farmer:")
    for key, value in farmer_data.items():
        print(f"  {key}: {value}")
    
    result = predict_yield_farmer_friendly(farmer_data)
    
    if result['success']:
        print(f"\n🎯 Predicted Yield: {result['predicted_yield']:.2f} {result['unit']}")
        print(f"🌍 Region Used: {result['region_used']}")
        print(f"⚙️  Number of defaulted parameters: {len(result['defaulted_parameters'])}")
        print("Defaulted parameters:", ", ".join(result['defaulted_parameters'][:5]) + "...")
    else:
        print(f"❌ Error: {result['error']}")

def example_3_detailed_input():
    """Example 3: Detailed input - farmer provides most parameters"""
    print("\n\n🌾 Example 3: Detailed Input")
    print("=" * 40)
    
    farmer_data = {
        "Area": "Brazil",
        "Item": "Soybean",
        "Year": 2024,
        "average_rain_fall_mm_per_year": 1200.0,
        "avg_temp": 26.5,
        "pesticides_tonnes": 90.0,
        "nitrogen": 110.0,
        "phosphorus": 35.0,
        "potassium": 160.0,
        "soil_ph": 5.8,
        "humidity": 78.0,
        "ndvi_avg": 0.75
    }
    
    print("Input provided by farmer:")
    for key, value in farmer_data.items():
        print(f"  {key}: {value}")
    
    result = predict_yield_farmer_friendly(farmer_data)
    
    if result['success']:
        print(f"\n🎯 Predicted Yield: {result['predicted_yield']:.2f} {result['unit']}")
        print(f"🌍 Region Used: {result['region_used']}")
        if result['defaulted_parameters']:
            print(f"⚙️  Number of defaulted parameters: {len(result['defaulted_parameters'])}")
            print("Defaulted parameters:", ", ".join(result['defaulted_parameters']))
        else:
            print("✅ All parameters provided by farmer!")
    else:
        print(f"❌ Error: {result['error']}")

def example_4_comparison():
    """Example 4: Compare predictions for different crops in the same region"""
    print("\n\n🌾 Example 4: Crop Comparison")
    print("=" * 40)
    
    area = "India"
    crops = ["Rice", "Wheat", "Corn"]
    
    print(f"Comparing crop yields in {area}:")
    
    for crop in crops:
        farmer_data = {
            "Area": area,
            "Item": crop
        }
        
        result = predict_yield_farmer_friendly(farmer_data)
        
        if result['success']:
            print(f"  {crop:8}: {result['predicted_yield']:8.2f} {result['unit']}")
        else:
            print(f"  {crop:8}: Error - {result['error']}")

def example_5_region_comparison():
    """Example 5: Compare the same crop in different regions"""
    print("\n\n🌾 Example 5: Region Comparison")
    print("=" * 40)
    
    crop = "Wheat"
    regions = ["India", "USA", "China", "Brazil"]
    
    print(f"Comparing {crop} yields in different regions:")
    
    for region in regions:
        farmer_data = {
            "Area": region,
            "Item": crop
        }
        
        result = predict_yield_farmer_friendly(farmer_data)
        
        if result['success']:
            print(f"  {region:8}: {result['predicted_yield']:8.2f} {result['unit']}")
        else:
            print(f"  {region:8}: Error - {result['error']}")

def main():
    print("🚜 Farmer-Friendly Crop Yield Prediction Examples")
    print("=" * 60)
    print("These examples show how farmers can use the system with")
    print("different levels of input, from minimal to detailed.")
    print()
    
    example_1_minimal_input()
    example_2_basic_input()
    example_3_detailed_input()
    example_4_comparison()
    example_5_region_comparison()
    
    print("\n\n💡 Key Benefits:")
    print("• Farmers can start with minimal information")
    print("• System uses regional defaults for soil parameters")
    print("• More detailed input improves accuracy")
    print("• Easy crop and region comparisons")
    print("• No need for expensive soil testing equipment")

if __name__ == "__main__":
    main()