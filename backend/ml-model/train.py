#!/usr/bin/env python3
"""
Crop Yield Prediction Model Training Script

This script trains a machine learning model to predict crop yields based on
soil, weather, and NDVI data.

Usage:
    python train.py --config config.yml
    python train.py --data_path data/processed/ --model_type xgboost
    python train.py --model_type random_forest --no_tuning
    python train.py --quick_demo  # Run with sample data

Features:
- Multiple model types (XGBoost, Random Forest, Linear, Ridge)
- Automated hyperparameter tuning
- Comprehensive model evaluation
- Feature importance analysis
- Cross-validation
- Model artifact saving
- Configuration management
"""

import argparse
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import GridSearchCV

# Import packages with proper error handling to avoid linter issues
import importlib
from typing import Any, Optional, Dict, List, Tuple, Union

# Module availability flags
SKLEARN_AVAILABLE = False
JOBLIB_AVAILABLE = False

# Import sklearn with error handling
try:
    sklearn_model_selection = importlib.import_module('sklearn.model_selection')
    sklearn_metrics = importlib.import_module('sklearn.metrics')
    sklearn_ensemble = importlib.import_module('sklearn.ensemble')
    sklearn_linear_model = importlib.import_module('sklearn.linear_model')
    sklearn_preprocessing = importlib.import_module('sklearn.preprocessing')
    SKLEARN_AVAILABLE = True
    print("✅ scikit-learn modules loaded successfully")
except ImportError:
    print("Warning: scikit-learn not available. Some ML functionality may not work.")
    print("Install with: pip install scikit-learn")
    SKLEARN_AVAILABLE = False

# Import joblib with error handling
try:
    joblib = importlib.import_module('joblib')
    JOBLIB_AVAILABLE = True
except ImportError:
    print("Warning: joblib not available. Model saving may not work.")
    print("Install with: pip install joblib")
    JOBLIB_AVAILABLE = False

# Try to import optional dependencies
try:
    yaml = importlib.import_module('yaml')
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    yaml = None
    print("Warning: PyYAML not available. Using JSON config fallback.")

try:
    xgb = importlib.import_module('xgboost')
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    xgb = None
    print("Warning: XGBoost not available. Will use alternative models.")

try:
    lgb = importlib.import_module('lightgbm')
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    lgb = None
    print("Warning: LightGBM not available.")

# Helper functions to get the right classes
def _get_train_test_split():
    if SKLEARN_AVAILABLE:
        return sklearn_model_selection.train_test_split
    else:
        raise ImportError("scikit-learn required for train_test_split")

def _get_grid_search_cv():
    if SKLEARN_AVAILABLE:
        return sklearn_model_selection.GridSearchCV
    else:
        raise ImportError("scikit-learn required for GridSearchCV")

def _get_cross_val_score():
    if SKLEARN_AVAILABLE:
        return sklearn_model_selection.cross_val_score
    else:
        raise ImportError("scikit-learn required for cross_val_score")

def _get_metrics():
    if SKLEARN_AVAILABLE:
        return {
            'mean_squared_error': sklearn_metrics.mean_squared_error,
            'mean_absolute_error': sklearn_metrics.mean_absolute_error,
            'r2_score': sklearn_metrics.r2_score
        }
    else:
        raise ImportError("scikit-learn required for metrics")

def _get_models():
    if SKLEARN_AVAILABLE:
        return {
            'RandomForestRegressor': sklearn_ensemble.RandomForestRegressor,
            'GradientBoostingRegressor': sklearn_ensemble.GradientBoostingRegressor,
            'LinearRegression': sklearn_linear_model.LinearRegression,
            'Ridge': sklearn_linear_model.Ridge,
            'Lasso': sklearn_linear_model.Lasso,
            'ElasticNet': sklearn_linear_model.ElasticNet,
            'StandardScaler': sklearn_preprocessing.StandardScaler,
            'RobustScaler': sklearn_preprocessing.RobustScaler,
            'LabelEncoder': sklearn_preprocessing.LabelEncoder
        }
    else:
        raise ImportError("scikit-learn required for models")

# Import custom utilities with proper error handling
try:
    from utils.preprocessing import DataPreprocessor, load_and_merge_datasets, validate_data_quality
    from utils.feature_engineering import FeatureEngineer, select_important_features
    UTILS_AVAILABLE = True
    print("✅ Custom preprocessing and feature engineering utilities loaded")
except ImportError as e:
    UTILS_AVAILABLE = False
    print(f"Warning: Custom utils not available ({e}). Using basic preprocessing.")
    # Create placeholder functions
    DataPreprocessor = None
    load_and_merge_datasets = None
    validate_data_quality = None
    FeatureEngineer = None
    select_important_features = None


def load_config(config_path):
    """Load configuration from YAML or JSON file"""
    if not os.path.exists(config_path):
        print(f"Config file {config_path} not found. Using default configuration.")
        return get_default_config()
    
    try:
        with open(config_path, 'r') as file:
            if config_path.endswith('.yml') or config_path.endswith('.yaml'):
                if YAML_AVAILABLE and yaml is not None:
                    config = yaml.safe_load(file)
                else:
                    print("YAML not available. Please use JSON config or install PyYAML.")
                    return get_default_config()
            else:
                config = json.load(file)
        
        print(f"✅ Configuration loaded from {config_path}")
        return config
        
    except Exception as e:
        print(f"Error loading config: {e}. Using default configuration.")
        return get_default_config()


def get_default_config():
    """Get default configuration"""
    return {
        'data': {
            'processed_data_path': 'data/processed/',
            'target_column': 'yield_value',
            'test_size': 0.2,
            'random_state': 42,
            'validation_split': 0.1
        },
        'preprocessing': {
            'handle_missing': True,
            'missing_strategy': 'median',
            'remove_outliers': True,
            'outlier_method': 'iqr',
            'scale_features': True,
            'scaling_method': 'robust',
            'handle_duplicates': True,
            'normalize_column_names': True,
            'encoding_method': 'onehot'
        },
        'feature_engineering': {
            'create_interactions': True,
            'create_polynomials': False,
            'polynomial_degree': 2,
            'create_temporal_features': True,
            'create_weather_features': True,
            'create_soil_features': True,
            'feature_selection': True,
            'max_features': 50
        },
        'model': {
            'type': 'random_forest',  # Changed default since XGBoost might not be available
            'hyperparameter_tuning': True,
            'cv_folds': 5,
            'scoring_metric': 'r2',
            'early_stopping': True
        },
        'output': {
            'model_save_path': 'models/',
            'save_preprocessing_objects': True,
            'save_feature_importance': True,
            'save_predictions': True
        },
        'logging': {
            'verbose': True,
            'save_logs': True
        }
    }


def load_data(data_path, target_column, quick_demo=False):
    """Load and prepare data for training"""
    print(f"📁 Loading data from {data_path}...")
    
    if quick_demo:
        print("⚡ Quick demo mode: Creating sample dataset...")
        return create_sample_data(target_column)
    
    # Try different file patterns
    data_files = [
        'comprehensive_dataset_fixed.csv',
        'integrated_dataset.csv',
        'merged_data.csv',
        'crop_yield_data.csv'
    ]
    
    df = None
    for filename in data_files:
        filepath = os.path.join(data_path, filename)
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                print(f"✅ Loaded {filename}: {df.shape}")
                break
            except Exception as e:
                print(f"⚠️ Error loading {filename}: {e}")
    
    # If no file found, try loading with utils
    if df is None and UTILS_AVAILABLE and load_and_merge_datasets is not None:
        try:
            df = load_and_merge_datasets(data_path)
            if not df.empty:
                print(f"✅ Loaded merged dataset: {df.shape}")
        except Exception as e:
            print(f"⚠️ Error with utils loading: {e}")
    
    # Last resort: create sample data
    if df is None or df.empty:
        print("⚠️ No data files found. Creating sample dataset for demonstration...")
        df = create_sample_data(target_column)
    
    # Validate target column
    if target_column not in df.columns:
        # Try to find similar column names
        possible_targets = [col for col in df.columns if any(word in col.lower() 
                          for word in ['yield', 'production', 'output'])]
        if possible_targets:
            print(f"⚠️ Target column '{target_column}' not found. Using '{possible_targets[0]}'")
            target_column = possible_targets[0]
        else:
            raise ValueError(f"Target column '{target_column}' not found in data. Available columns: {list(df.columns)}")
    
    # Basic data validation
    if UTILS_AVAILABLE and validate_data_quality is not None:
        quality_report = validate_data_quality(df, target_column)
        print(f"📊 Data Quality Score: {quality_report.get('quality_score', 'N/A')}/100")
    
    return df


def create_sample_data(target_column, n_samples=2000):
    """Create realistic sample data for demonstration"""
    print(f"🏭 Creating sample dataset with {n_samples} samples...")
    
    np.random.seed(42)
    
    # More realistic agricultural data
    areas = ['India', 'China', 'USA', 'Brazil', 'Argentina', 'Australia', 'Canada', 'Russia']
    crops = ['Wheat', 'Rice', 'Corn', 'Soybean', 'Barley', 'Cotton']
    
    data = {
        'Area': np.random.choice(areas, n_samples),
        'Item': np.random.choice(crops, n_samples),
        'Year': np.random.choice(range(2010, 2024), n_samples),
        'average_rain_fall_mm_per_year': np.random.uniform(300, 1500, n_samples),
        'avg_temp': np.random.uniform(15, 35, n_samples),
        'pesticides_tonnes': np.random.uniform(0, 500, n_samples),
        'soil_ph': np.random.uniform(5.5, 8.5, n_samples),
        'nitrogen': np.random.uniform(10, 50, n_samples),
        'phosphorus': np.random.uniform(5, 30, n_samples),
        'potassium': np.random.uniform(50, 200, n_samples),
        'organic_matter': np.random.uniform(1, 5, n_samples),
        'humidity': np.random.uniform(40, 90, n_samples),
        'sunshine_hours': np.random.uniform(1500, 3000, n_samples),
        'ndvi_avg': np.random.uniform(0.2, 0.8, n_samples),
        'elevation': np.random.uniform(0, 2000, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create realistic yield based on multiple factors with interactions
    base_yield = (
        df['nitrogen'] * 15 + 
        df['phosphorus'] * 12 + 
        df['potassium'] * 0.8 +
        df['average_rain_fall_mm_per_year'] * 0.8 + 
        df['avg_temp'] * 8 + 
        df['ndvi_avg'] * 800 + 
        df['organic_matter'] * 150 +
        df['humidity'] * 1.2 +
        (df['soil_ph'] - 6.5) ** 2 * -50  # Optimal pH around 6.5
    )
    
    # Add crop-specific multipliers
    crop_multipliers = {'Wheat': 1.0, 'Rice': 1.2, 'Corn': 1.1, 'Soybean': 0.9, 'Barley': 0.85, 'Cotton': 0.7}
    df['crop_multiplier'] = df['Item'].map(crop_multipliers.get)
    
    # Add area-specific effects (climate zones)
    area_effects = {'India': 1.1, 'China': 1.05, 'USA': 1.0, 'Brazil': 1.15, 
                   'Argentina': 1.0, 'Australia': 0.9, 'Canada': 0.95, 'Russia': 0.85}
    df['area_effect'] = df['Area'].map(area_effects.get)
    
    # Final yield calculation with noise
    df[target_column] = (
        base_yield * df['crop_multiplier'] * df['area_effect'] + 
        np.random.normal(0, 200, n_samples)  # Add realistic noise
    )
    
    # Ensure positive yields
    df[target_column] = np.maximum(df[target_column], 100)
    
    # Clean up temporary columns
    df = df.drop(['crop_multiplier', 'area_effect'], axis=1)
    
    print(f"✅ Sample dataset created: {df.shape}")
    print(f"🌾 Yield statistics: mean={df[target_column].mean():.1f}, std={df[target_column].std():.1f}")
    
    return df


def preprocess_data(df, config):
    """Preprocess data according to configuration"""
    print("🔧 Preprocessing data...")
    
    if UTILS_AVAILABLE and DataPreprocessor is not None:
        preprocessor = DataPreprocessor()
        
        # Use enhanced preprocessing pipeline
        df_processed, report = preprocessor.preprocess_pipeline(
            df,
            target_column=config['data']['target_column'],
            missing_strategy=config['preprocessing']['missing_strategy'],
            remove_outliers_flag=config['preprocessing']['remove_outliers'],
            scale_method=config['preprocessing']['scaling_method'],
            encoding_method=config['preprocessing']['encoding_method'],
            handle_duplicates_flag=config['preprocessing']['handle_duplicates'],
            normalize_names=config['preprocessing']['normalize_column_names']
        )
        
        print(f"✅ Preprocessing completed: {report['original_shape']} → {report['final_shape']}")
        print(f"📋 Steps completed: {len(report['steps_completed'])}")
        
    else:
        # Fallback basic preprocessing
        print("⚠️ Using basic preprocessing (utils not available)")
        preprocessor = BasicPreprocessor()
        
        # Handle missing values
        if config['preprocessing']['handle_missing']:
            df_processed = df.fillna(df.median(numeric_only=True))
            for col in df.select_dtypes(include=['object']).columns:
                df_processed[col] = df_processed[col].fillna(df_processed[col].mode()[0] if not df_processed[col].mode().empty else 'Unknown')
        else:
            df_processed = df.copy()
    
    # Feature engineering
    if config['feature_engineering']['create_interactions'] or \
       config['feature_engineering']['create_polynomials'] or \
       config['feature_engineering']['create_weather_features']:
        
        if UTILS_AVAILABLE and FeatureEngineer is not None:
            engineer = FeatureEngineer()
            df_processed = engineer.feature_engineering_pipeline(
                df_processed,
                include_interactions=config['feature_engineering']['create_interactions'],
                include_polynomials=config['feature_engineering']['create_polynomials'],
                include_climate=config['feature_engineering'].get('create_weather_features', True),
                include_water_stress=config['feature_engineering'].get('create_soil_features', True)
            )
            
            # Convert any categorical columns created by feature engineering to numeric
            categorical_cols = df_processed.select_dtypes(include=['category']).columns
            for col in categorical_cols:
                df_processed[col] = df_processed[col].cat.codes
                print(f"Converted categorical feature '{col}' to numeric codes")
            
            print(f"✨ Feature engineering completed: {df_processed.shape[1]} features")
        else:
            print("⚠️ Skipping advanced feature engineering (utils not available)")
    
    return df_processed, preprocessor


class BasicPreprocessor:
    """Basic preprocessing fallback when utils are not available"""
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
    
    def encode_categorical_variables(self, df):
        """Basic categorical encoding"""
        if SKLEARN_AVAILABLE:
            LabelEncoder = _get_models()['LabelEncoder']
        else:
            # Fallback to manual encoding
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                df[col] = pd.Categorical(df[col]).codes
                print(f"Encoded {col} using pandas categorical codes")
            return df
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col].astype(str))
            self.encoders[col] = encoder
            print(f"Encoded {col}: {len(encoder.classes_)} categories")
        return df
    
    def scale_features(self, df, method='robust'):
        """Basic feature scaling"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if SKLEARN_AVAILABLE:
            models = _get_models()
            if method == 'robust':
                scaler = models['RobustScaler']()
            else:
                scaler = models['StandardScaler']()
        else:
            # Fallback to manual scaling
            if method == 'robust':
                # Robust scaling using median and IQR
                for col in numeric_cols:
                    median = df[col].median()
                    q75 = df[col].quantile(0.75)
                    q25 = df[col].quantile(0.25)
                    iqr = q75 - q25
                    if iqr != 0:
                        df[col] = (df[col] - median) / iqr
            else:
                # Standard scaling using mean and std
                for col in numeric_cols:
                    mean = df[col].mean()
                    std = df[col].std()
                    if std != 0:
                        df[col] = (df[col] - mean) / std
            print(f"Scaled {len(numeric_cols)} features using manual {method} scaling")
            return df
        
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        self.scalers[method] = scaler
        print(f"Scaled {len(numeric_cols)} features using {method} scaling")
        return df


def train_model(X_train, y_train, model_type, hyperparameter_tuning=True, cv_folds=5, scoring='r2'):
    """Train machine learning model with enhanced options"""
    print(f"🎓 Training {model_type} model...")
    
    model_type = model_type.lower()
    
    # Get sklearn functions if available
    if SKLEARN_AVAILABLE:
        GridSearchCV = _get_grid_search_cv()
        models = _get_models()
    
    # XGBoost
    if model_type == 'xgboost' and XGBOOST_AVAILABLE and xgb is not None:
        if hyperparameter_tuning and SKLEARN_AVAILABLE:
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0]
            }
            
            model = xgb.XGBRegressor(random_state=42, n_jobs=-1)
            grid_search = GridSearchCV(
                model, param_grid, cv=cv_folds, scoring=scoring, n_jobs=-1, verbose=1
            )
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
            
            print(f"✅ Best parameters: {grid_search.best_params_}")
            print(f"🏆 Best CV score: {grid_search.best_score_:.3f}")
            
        else:
            best_model = xgb.XGBRegressor(
                n_estimators=200, max_depth=6, learning_rate=0.1, 
                subsample=0.9, colsample_bytree=0.9, random_state=42, n_jobs=-1
            )
            best_model.fit(X_train, y_train)
    
    # LightGBM
    elif model_type == 'lightgbm' and LIGHTGBM_AVAILABLE and lgb is not None:
        if hyperparameter_tuning and SKLEARN_AVAILABLE:
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0]
            }
            
            model = lgb.LGBMRegressor(random_state=42, n_jobs=-1, verbose=-1)
            grid_search = GridSearchCV(
                model, param_grid, cv=cv_folds, scoring=scoring, n_jobs=-1, verbose=1
            )
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
            
            print(f"✅ Best parameters: {grid_search.best_params_}")
            print(f"🏆 Best CV score: {grid_search.best_score_:.3f}")
        else:
            best_model = lgb.LGBMRegressor(
                n_estimators=200, max_depth=6, learning_rate=0.1, 
                subsample=0.9, colsample_bytree=0.9, random_state=42, n_jobs=-1, verbose=-1
            )
            best_model.fit(X_train, y_train)
            
    # Random Forest
    elif model_type == 'random_forest':
        if SKLEARN_AVAILABLE:
            RandomForestRegressor = models['RandomForestRegressor']
            if hyperparameter_tuning:
                # Reduced parameter grid for faster execution
                param_grid = {
                    'n_estimators': [100, 200],
                    'max_depth': [10, 20],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2],
                    'max_features': ['sqrt', 'log2']
                }
                
                model = RandomForestRegressor(random_state=42, n_jobs=1)  # Single job to avoid threading issues
                grid_search = GridSearchCV(
                    model, param_grid, cv=cv_folds, scoring=scoring, n_jobs=1, verbose=1  # Single job
                )
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
                
                print(f"✅ Best parameters: {grid_search.best_params_}")
                print(f"🏆 Best CV score: {grid_search.best_score_:.3f}")
                
            else:
                best_model = RandomForestRegressor(
                    n_estimators=200, max_depth=20, min_samples_split=5, 
                    min_samples_leaf=2, random_state=42, n_jobs=1  # Single job
                )
                best_model.fit(X_train, y_train)
        else:
            raise ImportError("scikit-learn required for RandomForestRegressor")
    
    # Gradient Boosting
    elif model_type == 'gradient_boosting':
        if SKLEARN_AVAILABLE:
            GradientBoostingRegressor = models['GradientBoostingRegressor']
            if hyperparameter_tuning:
                param_grid = {
                    'n_estimators': [100, 200, 300],
                    'max_depth': [3, 5, 7],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'subsample': [0.8, 0.9, 1.0]
                }
                
                model = GradientBoostingRegressor(random_state=42)
                grid_search = GridSearchCV(
                    model, param_grid, cv=cv_folds, scoring=scoring, n_jobs=-1, verbose=1
                )
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
                
                print(f"✅ Best parameters: {grid_search.best_params_}")
                print(f"🏆 Best CV score: {grid_search.best_score_:.3f}")
            else:
                best_model = GradientBoostingRegressor(
                    n_estimators=200, max_depth=5, learning_rate=0.1, 
                    subsample=0.9, random_state=42
                )
                best_model.fit(X_train, y_train)
        else:
            raise ImportError("scikit-learn required for GradientBoostingRegressor")
            
    # Linear Models
    elif model_type == 'linear':
        if SKLEARN_AVAILABLE:
            LinearRegression = models['LinearRegression']
            best_model = LinearRegression(n_jobs=-1)
            best_model.fit(X_train, y_train)
        else:
            raise ImportError("scikit-learn required for LinearRegression")
        
    elif model_type == 'ridge':
        if SKLEARN_AVAILABLE:
            Ridge = models['Ridge']
            if hyperparameter_tuning:
                param_grid = {'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}
                model = Ridge(random_state=42)
                grid_search = GridSearchCV(
                    model, param_grid, cv=cv_folds, scoring=scoring, n_jobs=-1
                )
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
                
                print(f"✅ Best parameters: {grid_search.best_params_}")
                print(f"🏆 Best CV score: {grid_search.best_score_:.3f}")
            else:
                best_model = Ridge(alpha=1.0, random_state=42)
                best_model.fit(X_train, y_train)
        else:
            raise ImportError("scikit-learn required for Ridge")
    
    elif model_type == 'lasso':
        if SKLEARN_AVAILABLE:
            Lasso = models['Lasso']
            if hyperparameter_tuning:
                param_grid = {'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}
                model = Lasso(random_state=42, max_iter=2000)
                grid_search = GridSearchCV(
                    model, param_grid, cv=cv_folds, scoring=scoring, n_jobs=-1
                )
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
                
                print(f"✅ Best parameters: {grid_search.best_params_}")
                print(f"🏆 Best CV score: {grid_search.best_score_:.3f}")
            else:
                best_model = Lasso(alpha=1.0, random_state=42, max_iter=2000)
                best_model.fit(X_train, y_train)
        else:
            raise ImportError("scikit-learn required for Lasso")
    
    elif model_type == 'elastic_net':
        if SKLEARN_AVAILABLE:
            ElasticNet = models['ElasticNet']
            if hyperparameter_tuning:
                param_grid = {
                    'alpha': [0.01, 0.1, 1.0, 10.0],
                    'l1_ratio': [0.1, 0.5, 0.7, 0.9]
                }
                model = ElasticNet(random_state=42, max_iter=2000)
                grid_search = GridSearchCV(
                    model, param_grid, cv=cv_folds, scoring=scoring, n_jobs=-1
                )
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
                
                print(f"✅ Best parameters: {grid_search.best_params_}")
                print(f"🏆 Best CV score: {grid_search.best_score_:.3f}")
            else:
                best_model = ElasticNet(alpha=1.0, l1_ratio=0.5, random_state=42, max_iter=2000)
                best_model.fit(X_train, y_train)
        else:
            raise ImportError("scikit-learn required for ElasticNet")
    
    else:
        # Fallback to Random Forest if requested model is not available
        print(f"⚠️ Model '{model_type}' not available. Using Random Forest instead.")
        best_model = RandomForestRegressor(
            n_estimators=200, max_depth=20, random_state=42, n_jobs=-1
        )
        best_model.fit(X_train, y_train)
    
    print(f"✅ Model training completed!")
    return best_model


def evaluate_model(model, X_test, y_test, model_name="Model"):
    """Comprehensive model evaluation"""
    print(f"📋 Evaluating {model_name} performance...")
    
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    if SKLEARN_AVAILABLE:
        metrics_funcs = _get_metrics()
        rmse = np.sqrt(metrics_funcs['mean_squared_error'](y_test, y_pred))
        mae = metrics_funcs['mean_absolute_error'](y_test, y_pred)
        r2 = metrics_funcs['r2_score'](y_test, y_pred)
    else:
        # Fallback manual metrics calculation
        rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
        mae = np.mean(np.abs(y_test - y_pred))
        ss_res = np.sum((y_test - y_pred) ** 2)
        ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
    
    # Avoid division by zero in MAPE
    mape = np.mean(np.abs((y_test - y_pred) / np.where(y_test == 0, 1, y_test))) * 100
    
    # Additional metrics
    explained_variance = 1 - np.var(y_test - y_pred) / np.var(y_test)
    max_error = np.max(np.abs(y_test - y_pred))
    
    metrics = {
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'mape': mape,
        'explained_variance': explained_variance,
        'max_error': max_error,
        'mean_actual': np.mean(y_test),
        'mean_predicted': np.mean(y_pred),
        'std_actual': np.std(y_test),
        'std_predicted': np.std(y_pred)
    }
    
    print(f"\n📊 {model_name} Performance Metrics:")
    print(f"  🏆 R² Score: {r2:.4f}")
    print(f"  📏 RMSE: {rmse:.3f}")
    print(f"  📎 MAE: {mae:.3f}")
    print(f"  📈 MAPE: {mape:.2f}%")
    print(f"  📊 Explained Variance: {explained_variance:.4f}")
    print(f"  ⚠️ Max Error: {max_error:.3f}")
    print(f"  🎯 Mean Actual: {metrics['mean_actual']:.3f}")
    print(f"  🎯 Mean Predicted: {metrics['mean_predicted']:.3f}")
    
    return metrics


def save_model_artifacts(model, preprocessor, feature_names, metrics, config, model_name="model"):
    """Save trained model and artifacts with enhanced metadata"""
    print("💾 Saving model artifacts...")
    
    save_path = config['output']['model_save_path']
    os.makedirs(save_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{config['model']['type']}_{model_name}_{timestamp}"
    
    # Save model
    model_filename = f"{base_name}.joblib"
    model_path = os.path.join(save_path, model_filename)
    joblib.dump(model, model_path)
    print(f"✅ Model saved: {model_filename}")
    
    # Save preprocessing objects
    if config['output']['save_preprocessing_objects']:
        if hasattr(preprocessor, 'scalers') and preprocessor.scalers:
            scaler_path = os.path.join(save_path, f"{base_name}_scalers.joblib")
            joblib.dump(preprocessor.scalers, scaler_path)
            print("✅ Scalers saved")
            
        if hasattr(preprocessor, 'encoders') and preprocessor.encoders:
            encoder_path = os.path.join(save_path, f"{base_name}_encoders.joblib")
            joblib.dump(preprocessor.encoders, encoder_path)
            print("✅ Encoders saved")
        
        # Save feature names
        feature_path = os.path.join(save_path, f"{base_name}_features.joblib")
        joblib.dump(feature_names, feature_path)
        print("✅ Feature names saved")
    
    # Save feature importance
    if config['output'].get('save_feature_importance', False) and hasattr(model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        importance_path = os.path.join(save_path, f"{base_name}_feature_importance.csv")
        importance_df.to_csv(importance_path, index=False)
        print("✅ Feature importance saved")
    
    # Save comprehensive metadata
    metadata = {
        'training_info': {
            'timestamp': datetime.now().isoformat(),
            'model_type': config['model']['type'],
            'features_count': len(feature_names),
            'hyperparameter_tuning': config['model']['hyperparameter_tuning'],
            'cv_folds': config['model']['cv_folds']
        },
        'data_info': {
            'target_column': config['data']['target_column'],
            'test_size': config['data']['test_size'],
            'preprocessing_steps': getattr(preprocessor, 'steps_completed', [])
        },
        'performance_metrics': metrics,
        'config': config,
        'model_files': {
            'model': model_filename,
            'scalers': f"{base_name}_scalers.joblib" if hasattr(preprocessor, 'scalers') and preprocessor.scalers else None,
            'encoders': f"{base_name}_encoders.joblib" if hasattr(preprocessor, 'encoders') and preprocessor.encoders else None,
            'features': f"{base_name}_features.joblib",
            'importance': f"{base_name}_feature_importance.csv" if hasattr(model, 'feature_importances_') else None
        }
    }
    
    metadata_path = os.path.join(save_path, f"{base_name}_metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)
    print("✅ Metadata saved")
    
    # Create a simple model info summary
    summary_path = os.path.join(save_path, f"{base_name}_summary.txt")
    with open(summary_path, 'w') as f:
        f.write(f"Crop Yield Prediction Model Summary\n")
        f.write(f"="*50 + "\n\n")
        f.write(f"Model Type: {config['model']['type']}\n")
        f.write(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Features Count: {len(feature_names)}\n")
        f.write(f"R² Score: {metrics['r2']:.4f}\n")
        f.write(f"RMSE: {metrics['rmse']:.3f}\n")
        f.write(f"MAE: {metrics['mae']:.3f}\n")
        f.write(f"MAPE: {metrics['mape']:.2f}%\n\n")
        
        if hasattr(model, 'feature_importances_'):
            f.write("Top 10 Important Features:\n")
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            for i, row in importance_df.head(10).iterrows():
                f.write(f"  {row['feature']}: {row['importance']:.4f}\n")
    
    print("✅ Model summary saved")
    
    return save_path, base_name


def main():
    """Enhanced main training function"""
    parser = argparse.ArgumentParser(
        description='Train crop yield prediction model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python train.py --quick_demo
  python train.py --model_type random_forest --no_tuning
  python train.py --data_path data/processed/ --model_type xgboost
  python train.py --config config.json --verbose
        """
    )
    
    parser.add_argument('--config', type=str, default='config.json',
                       help='Path to configuration file (JSON or YAML)')
    parser.add_argument('--data_path', type=str, default='data/processed/',
                       help='Path to processed data directory')
    parser.add_argument('--model_type', type=str, default='random_forest',
                       choices=['xgboost', 'lightgbm', 'random_forest', 'gradient_boosting', 
                               'linear', 'ridge', 'lasso', 'elastic_net'],
                       help='Type of model to train')
    parser.add_argument('--target_column', type=str, default='yield_value',
                       help='Name of target column')
    parser.add_argument('--no_tuning', action='store_true',
                       help='Skip hyperparameter tuning')
    parser.add_argument('--quick_demo', action='store_true',
                       help='Run quick demo with sample data')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--test_size', type=float, default=0.2,
                       help='Test set size (0.1-0.5)')
    parser.add_argument('--quick_training', action='store_true',
                       help='Use fast training settings to avoid long execution times')
    parser.add_argument('--cv_folds', type=int, default=5,
                       help='Number of cross-validation folds')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.data_path != 'data/processed/':
        config['data']['processed_data_path'] = args.data_path
    if args.model_type != 'random_forest':
        config['model']['type'] = args.model_type
    if args.target_column != 'yield_value':
        config['data']['target_column'] = args.target_column
    if args.no_tuning or args.quick_training:
        config['model']['hyperparameter_tuning'] = False
    if args.test_size != 0.2:
        config['data']['test_size'] = max(0.1, min(0.5, args.test_size))
    if args.cv_folds != 5:
        config['model']['cv_folds'] = max(2, min(10, args.cv_folds))
    
    print("🌾" + "="*58 + "🌾")
    print("   CROP YIELD PREDICTION MODEL TRAINING")
    print("🌾" + "="*58 + "🌾")
    print(f"🤖 Model Type: {config['model']['type'].upper()}")
    print(f"📊 Target: {config['data']['target_column']}")
    print(f"🔧 Hyperparameter Tuning: {'✅' if config['model']['hyperparameter_tuning'] else '❌'}")
    print(f"📋 Test Size: {config['data']['test_size']*100:.1f}%")
    print(f"🔄 CV Folds: {config['model']['cv_folds']}")
    
    # Check availability of requested model
    model_type = config['model']['type'].lower()
    if model_type == 'xgboost' and not XGBOOST_AVAILABLE:
        print(f"⚠️ XGBoost not available. Switching to Random Forest.")
        config['model']['type'] = 'random_forest'
    elif model_type == 'lightgbm' and not LIGHTGBM_AVAILABLE:
        print(f"⚠️ LightGBM not available. Switching to Random Forest.")
        config['model']['type'] = 'random_forest'
    
    try:
        # Load data
        df = load_data(
            config['data']['processed_data_path'], 
            config['data']['target_column'],
            quick_demo=args.quick_demo
        )
        
        if df.empty:
            raise ValueError("No data loaded. Please check data path or use --quick_demo.")
        
        # Preprocess data
        df_processed, preprocessor = preprocess_data(df, config)
        
        # Prepare features and target
        target_col = config['data']['target_column']
        if target_col not in df_processed.columns:
            raise ValueError(f"Target column '{target_col}' not found after preprocessing")
        
        # Separate features and target
        X = df_processed.drop(columns=[target_col])
        y = df_processed[target_col]
        
        print(f"📊 Dataset prepared: {X.shape[0]} samples, {X.shape[1]} features")
        
        # Encode categorical variables (if not done in preprocessing)
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            print(f"🔤 Encoding {len(categorical_cols)} categorical columns...")
            X = preprocessor.encode_categorical_variables(X)
            
            # Ensure all columns are numeric after encoding
            remaining_categorical = X.select_dtypes(include=['object', 'category']).columns
            if len(remaining_categorical) > 0:
                print(f"⚠️ Converting remaining categorical columns: {list(remaining_categorical)}")
                for col in remaining_categorical:
                    if X[col].dtype == 'object':
                        # Try to convert to numeric, fallback to label encoding
                        try:
                            X[col] = pd.to_numeric(X[col], errors='raise')
                        except:
                            from sklearn.preprocessing import LabelEncoder
                            le = LabelEncoder()
                            X[col] = le.fit_transform(X[col].astype(str))
                            print(f"  Label encoded {col}")
                    elif X[col].dtype.name == 'category':
                        X[col] = X[col].cat.codes
        
        # Feature selection (if enabled)
        if config['feature_engineering'].get('feature_selection', False) and UTILS_AVAILABLE:
            max_features = config['feature_engineering'].get('max_features', 50)
            if X.shape[1] > max_features:
                print(f"🎯 Selecting top {max_features} features...")
                try:
                    # Combine X and y temporarily for feature selection
                    temp_df = X.copy()
                    temp_df[target_col] = y
                    
                    selected_features = select_important_features(
                        temp_df, target_col, method='correlation', top_k=max_features
                    )
                    X = X[selected_features]
                    print(f"✅ Feature selection completed: {len(selected_features)} features selected")
                except Exception as e:
                    print(f"⚠️ Feature selection failed: {e}. Using all features.")
        
        # Train-test split
        if SKLEARN_AVAILABLE:
            train_test_split = _get_train_test_split()
        else:
            raise ImportError("scikit-learn required for train_test_split")
            
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=config['data']['test_size'],
            random_state=config['data']['random_state'],
            stratify=None  # For regression
        )
        
        # Scale features if specified
        if config['preprocessing']['scale_features']:
            print(f"⚖️ Scaling features using {config['preprocessing']['scaling_method']} method...")
            X_train = preprocessor.scale_features(
                X_train, method=config['preprocessing']['scaling_method']
            )
            X_test = preprocessor.scale_features(X_test, method=config['preprocessing']['scaling_method'])
        
        print(f"\n📋 Data Split Summary:")
        print(f"  Training set: {X_train.shape[0]} samples")
        print(f"  Test set: {X_test.shape[0]} samples")
        print(f"  Features: {X_train.shape[1]}")
        print(f"  Target mean: {y_train.mean():.2f} (train), {y_test.mean():.2f} (test)")
        
        # Train model
        model = train_model(
            X_train, y_train,
            config['model']['type'],
            config['model']['hyperparameter_tuning'],
            config['model']['cv_folds'],
            config['model'].get('scoring_metric', 'r2')
        )
        
        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test, config['model']['type'])
        
        # Cross-validation
        print(f"\n🔄 Cross-validation results:")
        if SKLEARN_AVAILABLE:
            cross_val_score = _get_cross_val_score()
            cv_scores = cross_val_score(
                model, X_train, y_train, 
                cv=config['model']['cv_folds'], 
                scoring=config['model'].get('scoring_metric', 'r2'),
                n_jobs=-1
            )
            print(f"  CV scores: {cv_scores}")
            print(f"  Mean CV score: {cv_scores.mean():.4f} (±{cv_scores.std() * 2:.4f})")
            
            # Add CV results to metrics
            metrics['cv_mean'] = cv_scores.mean()
            metrics['cv_std'] = cv_scores.std()
        else:
            print("  Cross-validation skipped (scikit-learn not available)")
            metrics['cv_mean'] = None
            metrics['cv_std'] = None
        
        # Feature importance analysis
        if hasattr(model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"\n🏆 Top 10 Important Features:")
            for i, row in feature_importance.head(10).iterrows():
                print(f"  {i+1:2d}. {row['feature']:<30} {row['importance']:.4f}")
        
        # Save model artifacts
        save_path, model_name = save_model_artifacts(
            model, preprocessor, list(X.columns), metrics, config, "crop_yield"
        )
        
        # Final summary
        print(f"\n🎆 Training completed successfully!")
        print(f"  💾 Model artifacts saved to: {save_path}")
        print(f"  🏆 Model performance: R² = {metrics['r2']:.4f}, RMSE = {metrics['rmse']:.3f}")
        print(f"  📊 Cross-validation: {metrics['cv_mean']:.4f} (±{metrics['cv_std']*2:.4f})")
        
        if metrics['r2'] > 0.8:
            print(f"  ⭐ Excellent model performance!")
        elif metrics['r2'] > 0.6:
            print(f"  🚀 Good model performance!")
        else:
            print(f"  📈 Model could be improved. Consider feature engineering or different algorithms.")
            
        print(f"\n🚀 Model is ready for deployment!")
        
    except Exception as e:
        print(f"\n❌ Training failed with error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())