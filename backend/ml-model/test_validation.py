#!/usr/bin/env python3
"""Test crop viability validation"""

from farmer_friendly_predict import predict_yield_farmer_friendly

def test_validation():
    print("🧪 TESTING CROP VIABILITY VALIDATION")
    print("=" * 50)
    
    # Test 1: Antarctica + Wheat (should fail)
    print("\n🧊 TEST 1: Antarctica + Wheat")
    result1 = predict_yield_farmer_friendly({
        'Area': 'Antarctica',
        'Item': 'Wheat',
        'Year': 2024
    })
    
    if result1['success']:
        print(f"❌ UNEXPECTED: Prediction succeeded - Yield: {result1['predicted_yield']}")
    else:
        print(f"✅ VALIDATION WORKED: {result1['error']}")
        if 'suggested_crops' in result1:
            print(f"💡 Suggested alternatives: {result1['suggested_crops']}")
    
    # Test 2: Normal location (should succeed)
    print("\n🌾 TEST 2: India + Wheat")
    result2 = predict_yield_farmer_friendly({
        'Area': 'India',
        'Item': 'Wheat',
        'Year': 2024
    })
    
    if result2['success']:
        print(f"✅ PREDICTION SUCCESSFUL: Yield: {result2['predicted_yield']:.2f} {result2.get('unit', 'hg/ha')}")
        print(f"🌍 Region: {result2['region_used']}")
        print(f"🌤️ Climate validation: {result2.get('climate_validation', 'N/A')}")
    else:
        print(f"❌ UNEXPECTED FAILURE: {result2['error']}")
    
    # Test 3: Desert + Rice (should fail or warn)
    print("\n🏜️ TEST 3: Sahara Desert + Rice")
    result3 = predict_yield_farmer_friendly({
        'Area': 'Sahara Desert',
        'Item': 'Rice',
        'Year': 2024
    })
    
    if result3['success']:
        print(f"⚠️ WARNING: Desert rice prediction succeeded - Yield: {result3['predicted_yield']}")
    else:
        print(f"✅ VALIDATION WORKED: {result3['error']}")
        if 'suggested_crops' in result3:
            print(f"💡 Suggested alternatives: {result3['suggested_crops']}")

if __name__ == "__main__":
    test_validation()