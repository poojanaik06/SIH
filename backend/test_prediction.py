from app.ml_service import get_ml_service, initialize_ml_service

def test_prediction_validation():
    """Test that the ML service properly validates inputs"""
    # Initialize the ML service first
    print("Initializing ML service...")
    init_result = initialize_ml_service()
    print(f"ML service initialized: {init_result}")
    
    ml = get_ml_service()
    
    print("=== Testing ML Service Input Validation ===")
    
    # Test 1: Empty data
    print("\n1. Testing with empty data:")
    result = ml.predict({})
    print(f"   Success: {result['success']}")
    print(f"   Error: {result.get('error', 'None')}")
    
    # Test 2: Incomplete data
    print("\n2. Testing with incomplete data:")
    result = ml.predict({'Area': 'India'})
    print(f"   Success: {result['success']}")
    print(f"   Error: {result.get('error', 'None')}")
    
    # Test 3: Complete data
    print("\n3. Testing with complete data:")
    result = ml.predict({
        'Area': 'India',
        'Item': 'Wheat', 
        'Year': 2024,
        'avg_temp': 25,
        'rainfall_mm': 800,
        'pesticide_tonnes': 120
    })
    print(f"   Success: {result['success']}")
    if result['success']:
        print(f"   Predicted Yield: {result.get('predicted_yield', 'None')}")
        print(f"   Input Used: {result.get('input_data_used', 'None')}")
    else:
        print(f"   Error: {result.get('error', 'None')}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_prediction_validation()