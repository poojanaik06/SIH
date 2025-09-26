#!/usr/bin/env python3

import pandas as pd
import numpy as np
import joblib
import json
import os
from typing import Dict, Any

def load_model_artifacts():
    """Load the trained model and its artifacts"""
    # Get the absolute path to the models directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, 'models')
    model_base_name = 'random_forest_crop_yield_20250926_143733'
    
    # Load model
    model_file = os.path.join(models_dir, f'{model_base_name}.joblib')
    model = joblib.load(model_file)
    
    # Load feature names
    features_file = os.path.join(models_dir, f'{model_base_name}_features.joblib')
    feature_names = joblib.load(features_file)
    
    # Load scalers
    scalers_file = os.path.join(models_dir, f'{model_base_name}_scalers.joblib')
    scalers = joblib.load(scalers_file) if os.path.exists(scalers_file) else None
    
    return model, feature_names, scalers

def create_features(data: Dict[str, Any]) -> pd.DataFrame:
    """Create all 50 features expected by the model"""
    
    # Start with a dictionary to build features
    features = {}
    
    # Basic features (direct mapping)
    features['year'] = data.get('Year', 2023)
    features['average_rain_fall_mm_per_year'] = data.get('average_rain_fall_mm_per_year', 1200.0)
    features['avg_temp'] = data.get('avg_temp', 25.0)
    features['pesticides_tonnes'] = data.get('pesticides_tonnes', 100.0)
    features['soil_ph'] = data.get('soil_ph', 6.5)
    features['nitrogen'] = data.get('nitrogen', 80.0)
    features['phosphorus'] = data.get('phosphorus', 40.0)
    features['potassium'] = data.get('potassium', 60.0)
    features['organic_matter'] = data.get('organic_matter', 3.0)
    features['humidity'] = data.get('humidity', 65.0)
    features['sunshine_hours'] = data.get('sunshine_hours', 8.0)
    features['ndvi_avg'] = data.get('ndvi_avg', 0.75)
    features['elevation'] = data.get('elevation', 500.0)
    features['vegetation_health'] = 3  # Healthy = 3
    features['light_intensity'] = 50000.0
    
    # Area one-hot encoding with improved location mapping
    area = data.get('Area', 'India')
    
    # Map specific locations to countries
    def map_location_to_country(location):
        location_lower = location.lower()
        
        # Indian locations
        indian_locations = ['mangalore', 'bangalore', 'mumbai', 'delhi', 'kolkata', 'chennai', 
                           'hyderabad', 'pune', 'goa', 'kerala', 'karnataka', 'gujarat', 
                           'maharashtra', 'punjab', 'haryana', 'uttar pradesh', 'rajasthan',
                           'bihar', 'west bengal', 'assam', 'odisha', 'tamil nadu', 'andhra pradesh']
        
        # US locations
        us_locations = ['california', 'texas', 'florida', 'new york', 'iowa', 'illinois', 
                       'kansas', 'nebraska', 'minnesota', 'wisconsin', 'michigan', 'ohio']
        
        # Chinese locations
        chinese_locations = ['beijing', 'shanghai', 'guangzhou', 'shenzhen', 'tianjin', 'chongqing']
        
        # Brazilian locations
        brazilian_locations = ['sao paulo', 'rio de janeiro', 'brasilia', 'salvador', 'fortaleza']
        
        # Australian locations
        australian_locations = ['sydney', 'melbourne', 'brisbane', 'perth', 'adelaide']
        
        # Canadian locations
        canadian_locations = ['toronto', 'vancouver', 'montreal', 'calgary', 'ottawa']
        
        # Russian locations
        russian_locations = ['moscow', 'saint petersburg', 'novosibirsk', 'yekaterinburg']
        
        # Check each category
        for loc in indian_locations:
            if loc in location_lower:
                return 'India'
        
        for loc in us_locations:
            if loc in location_lower:
                return 'USA'
                
        for loc in chinese_locations:
            if loc in location_lower:
                return 'China'
                
        for loc in brazilian_locations:
            if loc in location_lower:
                return 'Brazil'
                
        for loc in australian_locations:
            if loc in location_lower:
                return 'Australia'
                
        for loc in canadian_locations:
            if loc in location_lower:
                return 'Canada'
                
        for loc in russian_locations:
            if loc in location_lower:
                return 'Russia'
        
        # If India is mentioned anywhere in the location
        if 'india' in location_lower:
            return 'India'
        if 'usa' in location_lower or 'united states' in location_lower or 'america' in location_lower:
            return 'USA'
        if 'china' in location_lower:
            return 'China'
        if 'brazil' in location_lower:
            return 'Brazil'
        if 'australia' in location_lower:
            return 'Australia'
        if 'canada' in location_lower:
            return 'Canada'
        if 'russia' in location_lower or 'russian federation' in location_lower:
            return 'Russia'
            
        # If no match, return the original area
        return location
    
    # Map the area to a country
    mapped_area = map_location_to_country(area)
    
    area_mapping = {
        'Australia': 'area_Australia',
        'Brazil': 'area_Brazil', 
        'Canada': 'area_Canada',
        'China': 'area_China',
        'India': 'area_India',
        'Russian Federation': 'area_Russia',
        'Russia': 'area_Russia',
        'United States of America': 'area_USA',
        'USA': 'area_USA'
    }
    
    areas = ['area_Australia', 'area_Brazil', 'area_Canada', 'area_China', 'area_India', 'area_Russia', 'area_USA']
    for area_col in areas:
        features[area_col] = 0
    
    if mapped_area in area_mapping:
        features[area_mapping[mapped_area]] = 1
    else:
        # Default to India if no match found
        features['area_India'] = 1
    
    # Item one-hot encoding with improved crop mapping
    item = data.get('Item', 'Rice')
    
    # Normalize crop names
    def normalize_crop_name(crop):
        crop_lower = crop.lower().strip()
        
        # Map variations to standard names
        crop_mapping = {
            'rice': 'Rice',
            'paddy': 'Rice',
            'wheat': 'Wheat',
            'corn': 'Corn',
            'maize': 'Corn',  # Maize is corn
            'cotton': 'Cotton',
            'soybean': 'Soybean',
            'soybeans': 'Soybean',
            'soya': 'Soybean',
            'barley': 'Wheat',  # Map barley to wheat as closest match
            'sugarcane': 'Rice',  # Map to rice as fallback
            'potato': 'Rice',  # Map to rice as fallback
        }
        
        return crop_mapping.get(crop_lower, crop)  # Return normalized or original
    
    normalized_item = normalize_crop_name(item)
    
    item_mapping = {
        'Corn': 'item_Corn',
        'Cotton': 'item_Cotton',
        'Rice': 'item_Rice',
        'Soybean': 'item_Soybean',
        'Wheat': 'item_Wheat'
    }
    
    items = ['item_Corn', 'item_Cotton', 'item_Rice', 'item_Soybean', 'item_Wheat']
    for item_col in items:
        features[item_col] = 0
        
    if normalized_item in item_mapping:
        features[item_mapping[normalized_item]] = 1
    else:
        # Default to Rice if no match found
        features['item_Rice'] = 1
    
    # Engineered features
    features['n_p_ratio'] = features['nitrogen'] / (features['phosphorus'] + 0.001)
    features['n_k_ratio'] = features['nitrogen'] / (features['potassium'] + 0.001)
    features['p_k_ratio'] = features['phosphorus'] / (features['potassium'] + 0.001)
    features['nutrient_index'] = (features['nitrogen'] + features['phosphorus'] + features['potassium']) / 3
    
    # pH categories
    features['ph_acidic'] = 1 if features['soil_ph'] < 6.5 else 0
    features['ph_neutral'] = 1 if 6.5 <= features['soil_ph'] <= 7.5 else 0
    features['ph_alkaline'] = 1 if features['soil_ph'] > 7.5 else 0
    
    # Organic matter features
    features['high_organic_matter'] = 1 if features['organic_matter'] > 4.0 else 0
    features['organic_matter_squared'] = features['organic_matter'] ** 2
    
    # Vegetation and elevation features
    features['high_vegetation'] = 1 if features['vegetation_health'] >= 3 else 0
    features['high_elevation'] = 1 if features['elevation'] > 1000 else 0
    features['elevation_squared'] = features['elevation'] ** 2
    
    # Pesticide features
    features['pesticide_efficiency'] = features['pesticides_tonnes'] / (features['average_rain_fall_mm_per_year'] + 0.001)
    features['pesticide_intensity'] = features['pesticides_tonnes'] / 1000.0
    
    # Nitrogen efficiency
    features['nitrogen_use_efficiency'] = features['nitrogen'] / (features['average_rain_fall_mm_per_year'] + 0.001)
    
    # Cost and efficiency proxies
    features['total_input_cost_proxy'] = features['nitrogen'] + features['phosphorus'] + features['potassium'] + features['pesticides_tonnes']
    features['input_output_ratio'] = features['total_input_cost_proxy'] / (features['ndvi_avg'] + 0.001)
    
    # Climate cycles
    features['el_nino_cycle'] = float((features['year'] - 2000) % 7)
    features['decadal_climate_cycle'] = float((features['year'] - 2000) % 10)
    
    # Interaction features
    features['nitrogen_x_phosphorus'] = features['nitrogen'] * features['phosphorus']
    features['nitrogen_div_phosphorus'] = features['nitrogen'] / (features['phosphorus'] + 0.001)
    features['soil_ph_x_organic_matter'] = features['soil_ph'] * features['organic_matter']
    features['soil_ph_div_organic_matter'] = features['soil_ph'] / (features['organic_matter'] + 0.001)
    
    return pd.DataFrame([features])

def predict_yield(data: Dict[str, Any]) -> Dict[str, Any]:
    """Make a prediction using the trained model"""
    
    try:
        # Load model artifacts
        model, feature_names, scalers = load_model_artifacts()
        
        # Create features
        df = create_features(data)
        
        # Ensure all expected features are present in correct order
        df_aligned = df.reindex(columns=feature_names, fill_value=0)
        
        # Apply scaling if available - but only to numerical features
        if scalers and 'robust' in scalers:
            scaler = scalers['robust']
            
            # Get the features that the scaler was trained on
            scaler_features = scaler.feature_names_in_
            
            # Split into numerical and categorical features
            numerical_df = df_aligned[scaler_features]
            categorical_features = [col for col in feature_names if col not in scaler_features]
            categorical_df = df_aligned[categorical_features]
            
            # Scale only numerical features
            numerical_scaled = pd.DataFrame(
                scaler.transform(numerical_df),
                columns=numerical_df.columns
            )
            
            # Combine scaled numerical and unscaled categorical features
            df_final = pd.concat([numerical_scaled, categorical_df], axis=1)
            
            # Ensure correct order
            df_final = df_final.reindex(columns=feature_names, fill_value=0)
        else:
            df_final = df_aligned
        
        # Make prediction
        prediction = model.predict(df_final)[0]
        
        return {
            'success': True,
            'predicted_yield': float(prediction),
            'unit': 'hg/ha',
            'input_data': data,
            'message': 'Prediction completed successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'input_data': data
        }

if __name__ == '__main__':
    # Test with your data
    test_data = {
        "Area": "India",
        "Item": "Rice",
        "Year": 2023,
        "average_rain_fall_mm_per_year": 1200.0,
        "avg_temp": 25.5,
        "pesticides_tonnes": 100.0,
        "nitrogen": 80.0,
        "phosphorus": 40.0,
        "potassium": 60.0,
        "soil_ph": 6.5,
        "humidity": 0,
        "ndvi_avg": 0.75
    }
    
    print("🌾 Testing Direct Prediction")
    print("=" * 40)
    
    result = predict_yield(test_data)
    
    if result['success']:
        print("✅ SUCCESS!")
        print(f"🎯 Predicted Yield: {result['predicted_yield']:.2f} {result['unit']}")
    else:
        print("❌ ERROR!")
        print(f"💥 Error: {result['error']}")