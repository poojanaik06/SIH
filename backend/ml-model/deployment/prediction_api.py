# Crop Yield Prediction API
# Flask API for serving crop yield predictions

import sys
import os
# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from utils.preprocessing import DataPreprocessor, load_and_merge_datasets, validate_data_quality
from utils.feature_engineering import FeatureEngineer, select_important_features
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Global variables for model and preprocessor
model = None
preprocessor = None
feature_columns = None
data_preprocessor = None
feature_engineer = None

def load_model_artifacts():
    """Load trained model and preprocessor with utils integration"""
    global model, preprocessor, feature_columns, data_preprocessor, feature_engineer
    
    # Initialize utility classes
    data_preprocessor = DataPreprocessor()
    feature_engineer = FeatureEngineer()
    
    try:
        # Try to load saved model artifacts (use the working model from simple_predict.py)
        model = joblib.load('../../models/random_forest_crop_yield_20250925_224814.joblib')
        # Load the feature names that the model expects
        feature_columns = joblib.load('../../models/random_forest_crop_yield_20250925_224814_features.joblib')
        # Load scalers if available
        scalers_file = '../../models/random_forest_crop_yield_20250925_224814_scalers.joblib'
        scalers = joblib.load(scalers_file) if os.path.exists(scalers_file) else None
        preprocessor = scalers  # Use scalers as preprocessor
        print("✅ Model artifacts loaded successfully!")
        
        # Define basic input feature columns for API
        feature_columns = ['Area', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'avg_temp', 'pesticides_tonnes']
        
    except FileNotFoundError:
        print("⚠️ Model artifacts not found. Using fallback model with utils integration.")
        # Create fallback model using utils classes
        from sklearn.ensemble import RandomForestRegressor
        
        # Load sample data using utils
        try:
            # Use the correct processed data file from memory
            df = pd.read_csv('../data/processed/comprehensive_dataset_fixed.csv')
            print("✅ Data loaded directly from processed file")
        except:
            # Final fallback
            df = pd.read_csv('../data/processed/combined_dataset_cleaned.csv')
            print("✅ Data loaded from fallback processed file")
        
        # Clean data using DataPreprocessor
        df = data_preprocessor.handle_missing_values(df, strategy='median')
        
        # Validate data quality
        quality_report = validate_data_quality(df)
        print(f"✅ Data quality validated: {quality_report['status']}")
        
        # Apply feature engineering
        df = feature_engineer.create_weather_features(df)
        df = feature_engineer.create_soil_features(df)
        
        # Convert Year to datetime for temporal features, then back to numeric
        if 'Year' in df.columns:
            # Ensure Year is numeric first
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
            # Create a proper date column for temporal features
            df['date_temp'] = pd.to_datetime(df['Year'], format='%Y')
            df = feature_engineer.create_temporal_features(df, 'date_temp')
            # Drop the temporary date column
            df = df.drop('date_temp', axis=1)
        
        print("✅ Advanced features created using FeatureEngineer")
        
        # Define features
        target_column = 'yield_value'
        categorical_features = ['Area', 'Item']
        numerical_features = [col for col in df.columns if col not in categorical_features + [target_column] and col not in ['Unit']]
        
        # Create and fit preprocessor
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_features),
                ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
            ]
        )
        
        # Quick training with enhanced features
        df_sample = df.sample(n=min(5000, len(df)), random_state=42)
        X = df_sample.drop(target_column, axis=1)
        y = df_sample[target_column]
        
        X_processed = preprocessor.fit_transform(X)
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X_processed, y)
        
        print("✅ Enhanced fallback model created with feature engineering!")
        
        # Define expected feature columns (basic set for API)
        feature_columns = ['Area', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'avg_temp', 'pesticides_tonnes']

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'preprocessor_loaded': preprocessor is not None
    })

@app.route('/predict', methods=['POST'])
def predict_yield():
    """Predict crop yield based on input features"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Import the prediction function from simple_predict
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from simple_predict import predict_yield as simple_predict_yield
        
        # Use the working prediction function
        result = simple_predict_yield(data)
        
        if result['success']:
            return jsonify({
                'status': 'success',
                'predictions': [{
                    'input_data': data,
                    'predicted_yield': result['predicted_yield'],
                    'unit': result['unit'],
                    'confidence': 'high'
                }],
                'model_info': {
                    'model_type': 'RandomForestRegressor',
                    'features_used': 6
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'error': result['error']
            }), 500
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/predict/advanced', methods=['POST'])
def predict_yield_advanced():
    """Advanced prediction with feature engineering from utils"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Convert to DataFrame
        if isinstance(data, list):
            df_input = pd.DataFrame(data)
        else:
            df_input = pd.DataFrame([data])
        
        # Apply data preprocessing using utils
        df_processed = data_preprocessor.handle_missing_values(df_input.copy(), strategy='median')
        
        # Apply feature engineering using utils
        if 'temperature_max' in df_processed.columns or 'temperature_min' in df_processed.columns:
            df_processed = feature_engineer.create_weather_features(df_processed)
        
        if any(col in df_processed.columns for col in ['nitrogen', 'phosphorus', 'potassium', 'soil_ph']):
            df_processed = feature_engineer.create_soil_features(df_processed)
            
        if 'ndvi_avg' in df_processed.columns:
            df_processed = feature_engineer.create_ndvi_features(df_processed)
        
        # Apply temporal features if year is available
        if 'Year' in df_processed.columns:
            df_processed = feature_engineer.create_temporal_features(df_processed, 'Year')
        
        # Select only the features that the model expects
        available_features = [col for col in feature_columns if col in df_processed.columns]
        missing_features = [col for col in feature_columns if col not in df_processed.columns]
        
        if missing_features:
            return jsonify({
                'warning': f'Missing features: {missing_features}',
                'available_features': available_features,
                'using_fallback': True
            }), 200
        
        df_model_input = df_processed[available_features]
        
        # Fill missing values with smart defaults
        df_model_input = df_model_input.copy()
        if 'average_rain_fall_mm_per_year' in df_model_input.columns:
            df_model_input['average_rain_fall_mm_per_year'].fillna(800, inplace=True)
        if 'avg_temp' in df_model_input.columns:
            df_model_input['avg_temp'].fillna(20, inplace=True)
        if 'pesticides_tonnes' in df_model_input.columns:
            df_model_input['pesticides_tonnes'].fillna(0, inplace=True)
        
        # Preprocess and predict
        X_processed = preprocessor.transform(df_model_input)
        predictions = model.predict(X_processed)
        
        # Get feature importance if available
        feature_importance = None
        if hasattr(model, 'feature_importances_'):
            try:
                feature_names = (list(df_model_input.select_dtypes(include=[np.number]).columns) + 
                               list(preprocessor.named_transformers_['cat'].get_feature_names_out(['Area', 'Item'])))
                top_features = sorted(zip(feature_names, model.feature_importances_), 
                                    key=lambda x: x[1], reverse=True)[:5]
                feature_importance = {name: float(importance) for name, importance in top_features}
            except:
                feature_importance = "Feature importance calculation failed"
        
        # Prepare enhanced response
        results = []
        for i, pred in enumerate(predictions):
            result = {
                'input_data': df_input.iloc[i].to_dict(),
                'processed_features': df_processed.iloc[i].to_dict() if len(df_processed) > i else None,
                'predicted_yield': float(pred),
                'unit': 'hg/ha',
                'confidence': 'high' if len(available_features) == len(feature_columns) else 'medium',
                'features_used': len(available_features),
                'feature_engineering_applied': True
            }
            results.append(result)
        
        return jsonify({
            'status': 'success',
            'method': 'advanced_prediction_with_feature_engineering',
            'predictions': results,
            'feature_importance': feature_importance,
            'model_info': {
                'model_type': type(model).__name__,
                'utils_integration': True,
                'feature_engineering_enabled': True,
                'data_preprocessing_enabled': True
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'method': 'advanced_prediction'
        }), 500

@app.route('/predict/batch-advanced', methods=['POST'])
def predict_batch():
    """Batch prediction endpoint for multiple samples"""
    try:
        data = request.get_json()
        
        if not data or 'samples' not in data:
            return jsonify({'error': 'No samples provided. Use {"samples": [...]}'}), 400
        
        samples = data['samples']
        df_input = pd.DataFrame(samples)
        
        # Validate and process same as single prediction
        missing_cols = [col for col in feature_columns if col not in df_input.columns]
        if missing_cols:
            return jsonify({
                'error': f'Missing required columns: {missing_cols}',
                'required_columns': feature_columns
            }), 400
        
        df_input = df_input[feature_columns]
        
        # Fill missing values
        df_input['average_rain_fall_mm_per_year'].fillna(800, inplace=True)
        df_input['avg_temp'].fillna(20, inplace=True)
        df_input['pesticides_tonnes'].fillna(0, inplace=True)
        
        # Make predictions
        X_processed = preprocessor.transform(df_input)
        predictions = model.predict(X_processed)
        
        # Calculate batch statistics
        results = {
            'status': 'success',
            'batch_size': len(predictions),
            'predictions': [float(p) for p in predictions],
            'statistics': {
                'mean_yield': float(np.mean(predictions)),
                'min_yield': float(np.min(predictions)),
                'max_yield': float(np.max(predictions)),
                'std_yield': float(np.std(predictions))
            },
            'input_summary': {
                'areas': df_input['Area'].value_counts().to_dict(),
                'crops': df_input['Item'].value_counts().to_dict()
            }
        }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/data/validate', methods=['POST'])
def validate_input_data():
    """Validate input data quality using utils"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Convert to DataFrame
        if isinstance(data, list):
            df_input = pd.DataFrame(data)
        else:
            df_input = pd.DataFrame([data])
        
        # Use utils validation
        quality_report = validate_data_quality(df_input)
        
        # Additional validation using DataPreprocessor
        validation_results = {
            'status': 'success',
            'data_shape': df_input.shape,
            'quality_report': quality_report,
            'missing_values': df_input.isnull().sum().astype(int).to_dict(),
            'data_types': df_input.dtypes.astype(str).to_dict(),
            'numeric_summary': {k: {kk: float(vv) for kk, vv in v.items()} for k, v in df_input.describe().to_dict().items()} if not df_input.select_dtypes(include=[np.number]).empty else {},
            'recommendations': []
        }
        
        # Add recommendations
        missing_pct = (df_input.isnull().sum() / len(df_input) * 100)
        high_missing = missing_pct[missing_pct > 20].index.tolist()
        
        if high_missing:
            validation_results['recommendations'].append(
                f"High missing values in columns: {high_missing}. Consider data imputation."
            )
        
        required_cols = set(feature_columns)
        available_cols = set(df_input.columns)
        missing_required = required_cols - available_cols
        
        if missing_required:
            validation_results['recommendations'].append(
                f"Missing required columns for prediction: {list(missing_required)}"
            )
        
        return jsonify(validation_results)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
@app.route('/model/info', methods=['GET'])
def model_info():
    """Get information about the loaded model and utils integration"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    info = {
        'model_type': type(model).__name__,
        'features': feature_columns,
        'feature_count': len(feature_columns),
        'categorical_features': ['Area', 'Item'],
        'numerical_features': ['Year', 'average_rain_fall_mm_per_year', 'avg_temp', 'pesticides_tonnes'],
        'utils_integration': {
            'data_preprocessor': data_preprocessor is not None,
            'feature_engineer': feature_engineer is not None,
            'available_methods': [
                'handle_missing_values',
                'remove_outliers', 
                'encode_categorical_variables',
                'create_weather_features',
                'create_soil_features',
                'create_temporal_features'
            ]
        }
    }
    
    if hasattr(model, 'feature_importances_'):
        info['has_feature_importance'] = True
        info['n_features_in_model'] = len(model.feature_importances_)
    
    return jsonify(info)

if __name__ == '__main__':
    print("🚀 Starting Crop Yield Prediction API with Utils Integration...")
    load_model_artifacts()
    
    print("\n📋 API Endpoints:")
    print("  GET  /health              - Health check")
    print("  POST /predict             - Single prediction (basic)")
    print("  POST /predict/advanced    - Advanced prediction with feature engineering")
    print("  POST /predict/batch       - Batch predictions")
    print("  POST /data/validate       - Validate input data quality")
    print("  GET  /model/info          - Model and utils information")
    
    print("\n✨ Utils Integration Features:")
    print("  ✅ DataPreprocessor    - Advanced data cleaning")
    print("  ✅ FeatureEngineer     - Smart feature creation")
    print("  ✅ Data Quality Validation")
    print("  ✅ Advanced Weather Features")
    print("  ✅ Soil Feature Engineering")
    
    print("\n📝 Example requests:")
    print("\n1. Basic Prediction:")
    print("""curl -X POST http://localhost:5000/predict \\
      -H "Content-Type: application/json" \\
      -d '{
        "Area": "India",
        "Item": "Wheat",
        "Year": 2024,
        "average_rain_fall_mm_per_year": 800,
        "avg_temp": 25.5,
        "pesticides_tonnes": 150
      }'""")
    
    print("\n2. Advanced Prediction with Feature Engineering:")
    print("""curl -X POST http://localhost:5000/predict/advanced \\
      -H "Content-Type: application/json" \\
      -d '{
        "Area": "India",
        "Item": "Wheat",
        "Year": 2024,
        "temperature_max": 30,
        "temperature_min": 20,
        "rainfall": 800,
        "humidity": 65,
        "nitrogen": 120,
        "phosphorus": 80,
        "potassium": 200
      }'""")
    
    print("\n3. Data Validation:")
    print("""curl -X POST http://localhost:5000/data/validate \\
      -H "Content-Type: application/json" \\
      -d '{"Area": "India", "Item": "Wheat"}'""")
    
    app.run(debug=True, host='0.0.0.0', port=5000)