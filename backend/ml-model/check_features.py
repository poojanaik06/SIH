import joblib
import os

# Load feature names
models_dir = 'models'
model_base_name = 'random_forest_crop_yield_20250926_143733'
features_file = os.path.join(models_dir, f'{model_base_name}_features.joblib')

try:
    feature_names = joblib.load(features_file)
    print("Feature names:")
    for i, feature in enumerate(feature_names):
        print(f"{i+1:2d}. {feature}")
    print(f"\nTotal features: {len(feature_names)}")
except Exception as e:
    print(f"Error loading features: {e}")