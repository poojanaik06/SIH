import joblib

scalers = joblib.load('models/random_forest_crop_yield_20250926_143733_scalers.joblib')
features = joblib.load('models/random_forest_crop_yield_20250926_143733_features.joblib')

print('Scalers available:', list(scalers.keys()))
scaler = scalers['robust']
print('Scaler n_features:', scaler.n_features_in_)
print('Total features expected by model:', len(features))

if hasattr(scaler, 'feature_names_in_'):
    print('Scaler was trained with feature names')
    print('First 10 scaler features:', list(scaler.feature_names_in_)[:10])
else:
    print('Scaler was trained without feature names')

# Try a simple approach - skip scaling for categorical features
print('\nTrying to identify numeric vs categorical features...')
numeric_features = []
categorical_features = []

for i, feat in enumerate(features):
    if feat.startswith('area_') or feat.startswith('item_') or feat.startswith('ph_') or feat.startswith('high_'):
        categorical_features.append((i, feat))
    else:
        numeric_features.append((i, feat))

print(f'Numeric features: {len(numeric_features)}')
print(f'Categorical features: {len(categorical_features)}')
print(f'Scaler expects: {scaler.n_features_in_} features')

print('\nFirst 10 numeric features:')
for i, feat in numeric_features[:10]:
    print(f'  {i}: {feat}')