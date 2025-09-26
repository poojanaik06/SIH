#!/usr/bin/env python3
"""
Test script to verify weather-based prediction differences
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from farmer_friendly_predict import predict_yield_farmer_friendly

# Test different climate zones and weather conditions
test_cases = [
    # Different climate zones in India
    {"Area": "mumbai,india", "Item": "Rice", "area_type": "location", "description": "Coastal, High Humidity"},
    {"Area": "jodhpur,india", "Item": "Rice", "area_type": "location", "description": "Desert, Hot & Dry"},
    {"Area": "shimla,india", "Item": "Rice", "area_type": "location", "description": "Hill Station, Cool Climate"},
    {"Area": "kolkata,india", "Item": "Rice", "area_type": "location", "description": "Humid Subtropical"},
    {"Area": "punjab,india", "Item": "Rice", "area_type": "location", "description": "Fertile Plains"},
    
    # Different international locations
    {"Area": "california,usa", "Item": "Rice", "area_type": "location", "description": "Mediterranean Climate"},
    {"Area": "texas,usa", "Item": "Rice", "area_type": "location", "description": "Hot, Variable Rainfall"},
    {"Area": "bangkok,thailand", "Item": "Rice", "area_type": "location", "description": "Tropical, High Rainfall"},
    {"Area": "cairo,egypt", "Item": "Rice", "area_type": "location", "description": "Arid Desert Climate"},
    
    # Same location, different crops to test crop sensitivity
    {"Area": "mumbai,india", "Item": "Wheat", "area_type": "location", "description": "Coastal - Wheat"},
    {"Area": "mumbai,india", "Item": "Cotton", "area_type": "location", "description": "Coastal - Cotton"},
]

print("🌤️ Testing Weather-Based Yield Predictions")
print("=" * 90)
print(f"{'Location':<20} {'Crop':<8} {'Climate':<20} {'Yield':<12} {'Weather Conditions':<30}")
print("=" * 90)

results = []
for i, test_data in enumerate(test_cases, 1):
    result = predict_yield_farmer_friendly(test_data)
    
    if result['success']:
        yield_hg_ha = result['predicted_yield']
        weather = result.get('weather_conditions', {})
        temp = weather.get('temperature', 'N/A')
        rainfall = weather.get('rainfall', 'N/A')
        humidity = weather.get('humidity', 'N/A')
        
        weather_str = f"T:{temp:.1f}°C R:{rainfall:.0f}mm H:{humidity:.0f}%" if temp != 'N/A' else "No weather data"
        
        print(f"{test_data['Area']:<20} {test_data['Item']:<8} {test_data['description']:<20} {yield_hg_ha:<12.2f} {weather_str:<30}")
        
        results.append({
            'location': test_data['Area'],
            'crop': test_data['Item'],
            'yield': yield_hg_ha,
            'temp': temp,
            'rainfall': rainfall,
            'humidity': humidity,
            'description': test_data['description']
        })
    else:
        print(f"{test_data['Area']:<20} {test_data['Item']:<8} {test_data['description']:<20} {'ERROR':<12} {result.get('error', 'Unknown error'):<30}")

print("\n" + "=" * 90)
print("📈 WEATHER IMPACT ANALYSIS:")
print("=" * 90)

# Analyze weather impact
if results:
    rice_results = [r for r in results if r['crop'] == 'Rice']
    
    if len(rice_results) > 1:
        rice_yields = [r['yield'] for r in rice_results]
        min_yield = min(rice_yields)
        max_yield = max(rice_yields)
        yield_range = max_yield - min_yield
        
        print(f"Rice Yield Variation:")
        print(f"  • Minimum: {min_yield:.2f} hg/ha")
        print(f"  • Maximum: {max_yield:.2f} hg/ha") 
        print(f"  • Range: {yield_range:.2f} hg/ha ({yield_range/min_yield*100:.1f}% variation)")
        
        # Find best and worst conditions
        best_result = max(rice_results, key=lambda x: x['yield'])
        worst_result = min(rice_results, key=lambda x: x['yield'])
        
        print(f"\n🏆 Best Conditions for Rice:")
        print(f"  • Location: {best_result['location']} ({best_result['description']})")
        print(f"  • Yield: {best_result['yield']:.2f} hg/ha")
        if best_result['temp'] != 'N/A':
            print(f"  • Weather: {best_result['temp']:.1f}°C, {best_result['rainfall']:.0f}mm, {best_result['humidity']:.0f}% humidity")
        
        print(f"\n📉 Worst Conditions for Rice:")
        print(f"  • Location: {worst_result['location']} ({worst_result['description']})")
        print(f"  • Yield: {worst_result['yield']:.2f} hg/ha")
        if worst_result['temp'] != 'N/A':
            print(f"  • Weather: {worst_result['temp']:.1f}°C, {worst_result['rainfall']:.0f}mm, {worst_result['humidity']:.0f}% humidity")
    
    # Check if weather data is making a difference
    unique_yields = len(set(r['yield'] for r in results))
    if unique_yields > len(results) * 0.7:  # If most results are different
        print(f"\n✅ SUCCESS: Weather-based differentiation working!")
        print(f"   {unique_yields} different yield values out of {len(results)} predictions")
    else:
        print(f"\n⚠️  LIMITED VARIATION: Only {unique_yields} different yields from {len(results)} predictions")
        print(f"   Weather impact may need enhancement")

print(f"\n📊 Crop Comparison (Mumbai location):")
mumbai_results = [r for r in results if 'mumbai' in r['location'].lower()]
for result in mumbai_results:
    print(f"  • {result['crop']}: {result['yield']:.2f} hg/ha")