#!/usr/bin/env python3
"""
Direct prediction using your exact data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_predict import predict_yield

def main():
    # Your exact test data
    your_data = {
        "Area": "India",
        "Item": "Wheat",
        "Year": 2026,
        "average_rain_fall_mm_per_year": 1200,
        "avg_temp": 25.5,
        "pesticides_tonnes": 100,
        "nitrogen": 90,
        "phosphorus": 70,
        "potassium": 100,
        "soil_ph": 7.5,
        "humidity": 55,
        "ndvi_avg": 0.35,
        "organic_matter": 4.0
        # Note: vegetation_health, moisture, season_length are not needed
    }
    
    print("🌾 Predicting Crop Yield for Your Data")
    print("=" * 50)
    print("📊 Input Data:")
    for key, value in your_data.items():
        print(f"   {key}: {value}")
    print()
    
    # Make prediction
    result = predict_yield(your_data)
    
    print("📈 PREDICTION RESULT:")
    print("=" * 50)
    
    if result['success']:
        print(f"✅ SUCCESS!")
        print(f"🎯 Predicted Yield: {result['predicted_yield']:.2f} {result['unit']}")
        print(f"📝 Message: {result['message']}")
    else:
        print(f"❌ ERROR: {result['error']}")
    
    print("\n💡 This prediction uses a trained Random Forest model")
    print("   with 50 engineered features including soil, weather,")
    print("   and crop-specific characteristics.")

if __name__ == "__main__":
    main()