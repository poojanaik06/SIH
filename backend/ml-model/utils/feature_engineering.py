"""
Feature Engineering Utilities for Crop Yield Prediction

This module contains comprehensive functions for creating and engineering features
to improve machine learning model performance for crop yield prediction.

Key Features:
- Weather-based feature engineering
- Soil nutrient feature creation
- Temporal and seasonal features
- Geographic and climate features
- Water stress indicators
- Feature interaction and polynomial features
- Advanced aggregation features
- Economic efficiency indicators
- Extreme weather event detection
- Yield stability and trend analysis
- Automated feature selection
- Comprehensive feature analysis tools

Author: ML Model Development Team
Version: 2.0 - Complete Implementation
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import packages with proper error handling to avoid linter issues
import importlib
from typing import Any

# Module availability flags
SCIPY_AVAILABLE = False
SKLEARN_AVAILABLE = False

# Import scipy with error handling
try:
    scipy_stats = importlib.import_module('scipy.stats')
    SCIPY_AVAILABLE = True
except ImportError:
    print("Warning: scipy not available. Some statistical features may not work.")
    print("Install with: pip install scipy")
    scipy_stats = None

# Import sklearn with error handling
try:
    sklearn_preprocessing = importlib.import_module('sklearn.preprocessing')
    sklearn_feature_selection = importlib.import_module('sklearn.feature_selection')
    SKLEARN_AVAILABLE = True
except ImportError:
    print("Warning: scikit-learn not available. Some features may not work.")
    print("Install with: pip install scikit-learn")
    SKLEARN_AVAILABLE = False
    
    # Create fallback classes and functions
    class _DummyPolynomialFeatures:
        def __init__(self, degree=2, include_bias=False, **kwargs):
            self.degree = degree
            self.include_bias = include_bias
        
        def fit_transform(self, X):
            return X if hasattr(X, 'shape') else np.array(X)
        
        def get_feature_names_out(self, names):
            return list(names) if names is not None else []
    
    def _dummy_mutual_info_regression(X, y, **kwargs):
        """Fallback function when sklearn is not available"""
        if hasattr(X, 'shape'):
            return np.zeros(X.shape[1])
        return np.array([0.0])
    
    class _DummyVarianceThreshold:
        def __init__(self, threshold=0.0):
            self.threshold = threshold
        
        def fit(self, X):
            return self
        
        def get_support(self):
            return np.array([True])  # Fallback to include all features

# Helper functions to get the right classes/functions
def _get_polynomial_features():
    if SKLEARN_AVAILABLE:
        return sklearn_preprocessing.PolynomialFeatures
    else:
        return _DummyPolynomialFeatures

def _get_mutual_info_regression():
    if SKLEARN_AVAILABLE:
        return sklearn_feature_selection.mutual_info_regression
    else:
        return _dummy_mutual_info_regression

def _get_variance_threshold():
    if SKLEARN_AVAILABLE:
        return sklearn_feature_selection.VarianceThreshold
    else:
        return _DummyVarianceThreshold


class FeatureEngineer:
    """
    Feature engineering class for crop yield prediction
    """
    
    def __init__(self):
        self.polynomial_features = None
        self.feature_stats = {}
    
    def create_weather_features(self, df):
        """
        Create derived weather features
        
        Args:
            df: DataFrame with weather data
        
        Returns:
            DataFrame with additional weather features
        """
        print("Creating weather-based features...")
        
        # Temperature-based features
        if 'temperature_max' in df.columns and 'temperature_min' in df.columns:
            df['temperature_range'] = df['temperature_max'] - df['temperature_min']
            df['temperature_avg'] = (df['temperature_max'] + df['temperature_min']) / 2
            
        # Growing Degree Days (GDD)
        if 'temperature_avg' in df.columns:
            base_temp = 10  # Base temperature for crop growth
            df['growing_degree_days'] = np.maximum(0, df['temperature_avg'] - base_temp)
            
        # Heat stress indicator
        if 'temperature_max' in df.columns:
            heat_threshold = 35  # Heat stress threshold
            df['heat_stress_days'] = (df['temperature_max'] > heat_threshold).astype(int)
            
        # Humidity and temperature interaction
        if 'humidity' in df.columns and 'temperature_avg' in df.columns:
            df['heat_index'] = df['temperature_avg'] + (df['humidity'] / 100) * 10
            df['vapor_pressure_deficit'] = self._calculate_vpd(df['temperature_avg'], df['humidity'])
        
        # Rainfall patterns
        if 'rainfall' in df.columns:
            df['rainfall_squared'] = df['rainfall'] ** 2
            df['is_drought'] = (df['rainfall'] < 10).astype(int)  # Less than 10mm
            df['is_heavy_rain'] = (df['rainfall'] > 50).astype(int)  # More than 50mm
            
        # Sunshine hours features
        if 'sunshine_hours' in df.columns:
            df['light_intensity'] = df['sunshine_hours'] / 24  # Proportion of day with sun
            
        print(f"Created weather features. New shape: {df.shape}")
        return df
    
    def create_soil_features(self, df):
        """
        Create derived soil features
        
        Args:
            df: DataFrame with soil data
        
        Returns:
            DataFrame with additional soil features
        """
        print("Creating soil-based features...")
        
        # Nutrient ratios
        if 'nitrogen' in df.columns and 'phosphorus' in df.columns:
            df['n_p_ratio'] = df['nitrogen'] / (df['phosphorus'] + 1)  # +1 to avoid division by zero
            
        if 'nitrogen' in df.columns and 'potassium' in df.columns:
            df['n_k_ratio'] = df['nitrogen'] / (df['potassium'] + 1)
            
        if 'phosphorus' in df.columns and 'potassium' in df.columns:
            df['p_k_ratio'] = df['phosphorus'] / (df['potassium'] + 1)
        
        # Nutrient index
        if all(col in df.columns for col in ['nitrogen', 'phosphorus', 'potassium']):
            df['nutrient_index'] = (df['nitrogen'] + df['phosphorus'] + df['potassium']) / 3
            
        # Soil pH categories
        if 'soil_ph' in df.columns:
            df['ph_acidic'] = (df['soil_ph'] < 6.0).astype(int)
            df['ph_neutral'] = ((df['soil_ph'] >= 6.0) & (df['soil_ph'] <= 7.5)).astype(int)
            df['ph_alkaline'] = (df['soil_ph'] > 7.5).astype(int)
            
        # Organic matter categories
        if 'organic_matter' in df.columns:
            df['high_organic_matter'] = (df['organic_matter'] > 3.0).astype(int)
            df['organic_matter_squared'] = df['organic_matter'] ** 2
            
        print(f"Created soil features. New shape: {df.shape}")
        return df
    
    def create_ndvi_features(self, df):
        """
        Create derived NDVI and vegetation features
        
        Args:
            df: DataFrame with NDVI data
        
        Returns:
            DataFrame with additional vegetation features
        """
        print("Creating NDVI-based features...")
        
        # NDVI statistics (if multiple NDVI values per location)
        if 'ndvi_value' in df.columns:
            df['ndvi_squared'] = df['ndvi_value'] ** 2
            df['ndvi_log'] = np.log1p(df['ndvi_value'])  # log(1 + x) to handle zeros
            
        # NDVI categories
        if 'ndvi_avg' in df.columns:
            df['vegetation_health'] = pd.cut(df['ndvi_avg'], 
                                           bins=[0, 0.2, 0.4, 0.6, 1.0],
                                           labels=['poor', 'fair', 'good', 'excellent'])
            df['high_vegetation'] = (df['ndvi_avg'] > 0.6).astype(int)
            
        # Seasonal NDVI features (if date information available)
        if 'month' in df.columns and 'ndvi_avg' in df.columns:
            df['ndvi_seasonal'] = df['ndvi_avg'] * np.sin(2 * np.pi * df['month'] / 12)
            
        print(f"Created NDVI features. New shape: {df.shape}")
        return df
    
    def create_geographic_features(self, df):
        """
        Create geographic and location-based features
        
        Args:
            df: DataFrame with location data
        
        Returns:
            DataFrame with additional geographic features
        """
        print("Creating geographic features...")
        
        # Climate zones based on latitude
        if 'latitude' in df.columns:
            df['climate_zone'] = pd.cut(df['latitude'],
                                      bins=[-90, 23.5, 66.5, 90],
                                      labels=['tropical', 'temperate', 'polar'])
            df['abs_latitude'] = np.abs(df['latitude'])
            
        # Elevation categories
        if 'elevation' in df.columns:
            df['high_elevation'] = (df['elevation'] > 1000).astype(int)
            df['elevation_squared'] = df['elevation'] ** 2
            
        # Distance from equator (affects growing conditions)
        if 'latitude' in df.columns:
            df['distance_from_equator'] = np.abs(df['latitude'])
            
        print(f"Created geographic features. New shape: {df.shape}")
        return df
    
    def create_temporal_features(self, df, date_column='date'):
        """
        Create time-based features
        
        Args:
            df: DataFrame with date information
            date_column: name of date column
        
        Returns:
            DataFrame with temporal features
        """
        print("Creating temporal features...")
        
        if date_column in df.columns:
            # Handle different date column types
            if df[date_column].dtype == 'object' or df[date_column].dtype == 'int64':
                if df[date_column].dtype == 'int64':
                    # If it's a year column
                    df['year'] = df[date_column]
                    df['month'] = 6  # Assume mid-year for annual data
                    df['day_of_year'] = 180  # Mid-year day
                    df['quarter'] = 2  # Q2
                else:
                    df[date_column] = pd.to_datetime(df[date_column])
                    # Basic date features
                    df['year'] = df[date_column].dt.year
                    df['month'] = df[date_column].dt.month
                    df['day_of_year'] = df[date_column].dt.dayofyear
                    df['quarter'] = df[date_column].dt.quarter
            else:
                # Already datetime
                df['year'] = df[date_column].dt.year
                df['month'] = df[date_column].dt.month
                df['day_of_year'] = df[date_column].dt.dayofyear
                df['quarter'] = df[date_column].dt.quarter
            
            # Cyclical features
            df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
            df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
            df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
            df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
            
            # Growing season indicator (Northern Hemisphere)
            df['growing_season'] = ((df['month'] >= 4) & (df['month'] <= 9)).astype(int)
            
            # Years since reference year
            reference_year = df['year'].min()
            df['years_since_start'] = df['year'] - reference_year
            
            # Decade feature
            df['decade'] = (df['year'] // 10) * 10
            
            # Is leap year
            df['is_leap_year'] = ((df['year'] % 4 == 0) & 
                                 ((df['year'] % 100 != 0) | (df['year'] % 400 == 0))).astype(int)
            
            # Season categories
            df['season'] = df['month'].apply(self._get_season)
            
        elif 'Year' in df.columns:
            # Handle Year column specifically
            df['year'] = df['Year']
            df['month'] = 6  # Assume mid-year for annual data
            df['day_of_year'] = 180  # Mid-year day
            df['quarter'] = 2  # Q2
            
            # Cyclical features
            df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
            df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
            df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
            df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
            
            # Growing season indicator
            df['growing_season'] = 1  # Assume growing season for annual data
            
            # Years since reference year
            reference_year = df['year'].min()
            df['years_since_start'] = df['year'] - reference_year
            
            # Decade feature
            df['decade'] = (df['year'] // 10) * 10
            
            # Is leap year
            df['is_leap_year'] = ((df['year'] % 4 == 0) & 
                                 ((df['year'] % 100 != 0) | (df['year'] % 400 == 0))).astype(int)
        print(f"Created temporal features. New shape: {df.shape}")
        return df
    
    def _get_season(self, month):
        """Helper function to determine season from month"""
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'
    
    def create_interaction_features(self, df, feature_pairs=None):
        """
        Create interaction features between variables
        
        Args:
            df: DataFrame
            feature_pairs: list of tuples with feature pairs to interact
        
        Returns:
            DataFrame with interaction features
        """
        print("Creating interaction features...")
        
        if feature_pairs is None:
            # Default important interactions for crop yield
            feature_pairs = [
                ('rainfall', 'temperature_avg'),
                ('nitrogen', 'phosphorus'),
                ('soil_ph', 'organic_matter'),
                ('ndvi_avg', 'rainfall'),
                ('temperature_avg', 'humidity')
            ]
        
        for feature1, feature2 in feature_pairs:
            if feature1 in df.columns and feature2 in df.columns:
                df[f'{feature1}_x_{feature2}'] = df[feature1] * df[feature2]
                df[f'{feature1}_div_{feature2}'] = df[feature1] / (df[feature2] + 1)
        
        print(f"Created interaction features. New shape: {df.shape}")
        return df
    
    def create_polynomial_features(self, df, columns=None, degree=2):
        """
        Create polynomial features
        
        Args:
            df: DataFrame
            columns: list of columns to create polynomials for
            degree: polynomial degree
        
        Returns:
            DataFrame with polynomial features
        """
        print(f"Creating polynomial features (degree {degree})...")
        
        if columns is None:
            columns = ['rainfall', 'temperature_avg', 'nitrogen', 'ndvi_avg']
            columns = [col for col in columns if col in df.columns]
        
        if len(columns) > 0:
            PolynomialFeatures = _get_polynomial_features()
            self.polynomial_features = PolynomialFeatures(degree=degree, include_bias=False)
            poly_data = self.polynomial_features.fit_transform(df[columns])
            
            # Get feature names
            try:
                feature_names = self.polynomial_features.get_feature_names_out(columns)
            except AttributeError:
                # Fallback for older sklearn versions or dummy class
                feature_names = [f"poly_{i}" for i in range(poly_data.shape[1])]
            
            # Add polynomial features to dataframe
            poly_df = pd.DataFrame(poly_data, index=df.index)
            poly_df.columns = list(feature_names)
            df = pd.concat([df, poly_df.iloc[:, len(columns):]], axis=1)  # Exclude original features
        
        print(f"Created polynomial features. New shape: {df.shape}")
        return df
    
    def create_lag_features(self, df, columns=None, lags=[1, 2, 3]):
        """
        Create lag features for time series data
        
        Args:
            df: DataFrame (should be sorted by date)
            columns: list of columns to create lags for
            lags: list of lag periods
        
        Returns:
            DataFrame with lag features
        """
        print("Creating lag features...")
        
        if columns is None:
            columns = ['rainfall', 'temperature_avg', 'ndvi_avg']
            columns = [col for col in columns if col in df.columns]
        
        for col in columns:
            for lag in lags:
                df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        
        print(f"Created lag features. New shape: {df.shape}")
        return df
    
    def create_statistical_features(self, df, window_size=7):
        """
        Create rolling statistical features
        
        Args:
            df: DataFrame
            window_size: window size for rolling statistics
        
        Returns:
            DataFrame with statistical features
        """
        print(f"Creating rolling statistical features (window={window_size})...")
        
        numeric_cols = ['rainfall', 'temperature_avg', 'humidity', 'ndvi_avg']
        numeric_cols = [col for col in numeric_cols if col in df.columns]
        
        for col in numeric_cols:
            df[f'{col}_rolling_mean'] = df[col].rolling(window=window_size).mean()
            df[f'{col}_rolling_std'] = df[col].rolling(window=window_size).std()
            df[f'{col}_rolling_max'] = df[col].rolling(window=window_size).max()
            df[f'{col}_rolling_min'] = df[col].rolling(window=window_size).min()
        
        print(f"Created statistical features. New shape: {df.shape}")
        return df
    
    def feature_engineering_pipeline(self, df: pd.DataFrame, include_interactions: bool = True, 
                                   include_polynomials: bool = False, include_lags: bool = False,
                                   include_climate: bool = True, include_water_stress: bool = True,
                                   include_advanced_aggregations: bool = True, include_economic: bool = True,
                                   include_seasonal_patterns: bool = True, include_extreme_events: bool = True,
                                   include_yield_stability: bool = False) -> pd.DataFrame:
        """
        Complete feature engineering pipeline with advanced features
        
        Args:
            df: input DataFrame
            include_interactions: whether to create interaction features
            include_polynomials: whether to create polynomial features
            include_lags: whether to create lag features
            include_climate: whether to create climate features
            include_water_stress: whether to create water stress features
            include_advanced_aggregations: whether to create aggregation features
            include_economic: whether to create economic efficiency features
            include_seasonal_patterns: whether to create advanced seasonal features
            include_extreme_events: whether to create extreme weather event features
            include_yield_stability: whether to create yield stability features (requires historical data)
        
        Returns:
            DataFrame with engineered features
        """
        print("Starting comprehensive feature engineering pipeline...")
        print(f"Input shape: {df.shape}")
        
        # Create domain-specific features
        df = self.create_weather_features(df)
        df = self.create_soil_features(df)
        df = self.create_ndvi_features(df)
        df = self.create_geographic_features(df)
        
        # Create temporal features if date column exists
        if 'date' in df.columns or 'Year' in df.columns:
            date_col = 'date' if 'date' in df.columns else 'Year'
            df = self.create_temporal_features(df, date_col)
        
        # Create additional climate features
        if include_climate:
            df = self.create_climate_features(df)
        
        # Create water stress features
        if include_water_stress:
            df = self.create_water_stress_features(df)
        
        # Create advanced aggregation features
        if include_advanced_aggregations:
            df = self.create_advanced_aggregations(df)
        
        # Create economic efficiency features
        if include_economic:
            df = self.create_economic_features(df)
        
        # Create advanced seasonal patterns
        if include_seasonal_patterns:
            df = self.create_seasonal_patterns(df)
        
        # Create extreme weather event features
        if include_extreme_events:
            df = self.create_extreme_event_features(df)
        
        # Create yield stability features (for historical analysis)
        if include_yield_stability:
            df = self.create_yield_stability_features(df)
        
        # Create interaction features
        if include_interactions:
            df = self.create_interaction_features(df)
        
        # Create polynomial features
        if include_polynomials:
            df = self.create_polynomial_features(df)
        
        # Create lag features (for time series)
        if include_lags and 'date' in df.columns:
            df = self.create_lag_features(df)
        
        # Handle any infinite or very large values
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # Fill NaN values created during feature engineering
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Feature count for summary
        original_features = ['Area', 'Item', 'Year', 'rainfall', 'temperature_avg', 'nitrogen', 
                           'phosphorus', 'potassium', 'soil_ph', 'yield_value']
        features_added = df.shape[1] - len([col for col in original_features if col in df.columns])
        
        print("Feature engineering pipeline completed!")
        print(f"Final shape: {df.shape}")
        print(f"Features added: {features_added}")
        
        return df
    
    def _calculate_vpd(self, temp, humidity):
        """
        Calculate Vapor Pressure Deficit
        
        Args:
            temp: temperature in Celsius
            humidity: relative humidity in percentage
        
        Returns:
            VPD values
        """
        # Saturation vapor pressure (kPa) using Tetens formula
        es = 0.6108 * np.exp(17.27 * temp / (temp + 237.3))
        
        # Actual vapor pressure (kPa)
        ea = es * (humidity / 100)
        
        # Vapor pressure deficit (kPa)
        vpd = es - ea
        
        return np.maximum(vpd, 0)  # Ensure non-negative values
    
    def create_climate_features(self, df):
        """
        Create climate-related features
        
        Args:
            df: DataFrame with climate data
        
        Returns:
            DataFrame with climate features
        """
        print("Creating climate features...")
        
        # Aridity index (if both rainfall and temperature are available)
        if 'rainfall' in df.columns and 'temperature_avg' in df.columns:
            # Simple aridity index: rainfall / potential evapotranspiration
            pet = 16 * (10 * df['temperature_avg'] / 12) ** 1.25  # Thornthwaite method approximation
            df['aridity_index'] = df['rainfall'] / (pet + 1)  # +1 to avoid division by zero
            df['is_arid'] = (df['aridity_index'] < 0.5).astype(int)
            df['is_humid'] = (df['aridity_index'] > 1.5).astype(int)
        
        # Frost risk
        if 'temperature_min' in df.columns:
            df['frost_risk'] = (df['temperature_min'] < 0).astype(int)
            df['freeze_risk'] = (df['temperature_min'] < -5).astype(int)
        
        # Growing degree days with different base temperatures
        if 'temperature_avg' in df.columns:
            for base_temp in [5, 10, 15]:
                df[f'gdd_base_{base_temp}'] = np.maximum(0, df['temperature_avg'] - base_temp)
        
        # Chill hours (important for fruit trees)
        if 'temperature_min' in df.columns and 'temperature_max' in df.columns:
            # Approximate chill hours (hours between 0-7°C)
            df['chill_hours'] = np.where(
                (df['temperature_min'] <= 7) & (df['temperature_max'] >= 0),
                24 * (7 - np.maximum(0, df['temperature_min'])) / 
                (df['temperature_max'] - df['temperature_min'] + 1),
                0
            )
        
        print(f"Created climate features. New shape: {df.shape}")
        return df
    
    def create_water_stress_features(self, df):
        """
        Create water stress related features
        
        Args:
            df: DataFrame with water-related data
        
        Returns:
            DataFrame with water stress features
        """
        print("Creating water stress features...")
        
        # Water balance features
        if 'rainfall' in df.columns and 'temperature_avg' in df.columns:
            # Simple water balance (precipitation - evapotranspiration)
            pet = 16 * (10 * df['temperature_avg'] / 12) ** 1.25  # Simplified PET
            df['water_balance'] = df['rainfall'] - pet
            df['water_deficit'] = np.minimum(0, df['water_balance'])
            df['water_surplus'] = np.maximum(0, df['water_balance'])
        
        # Drought severity index
        if 'rainfall' in df.columns:
            # Calculate rolling mean for drought assessment
            if len(df) > 30:
                df['rainfall_30day_mean'] = df['rainfall'].rolling(window=30, min_periods=1).mean()
                df['drought_severity'] = (df['rainfall_30day_mean'] - df['rainfall'].mean()) / df['rainfall'].std()
            else:
                df['drought_severity'] = (df['rainfall'] - df['rainfall'].mean()) / (df['rainfall'].std() + 1e-6)
        
        # Consecutive dry days
        if 'rainfall' in df.columns:
            dry_days = (df['rainfall'] < 1).astype(int)
            df['consecutive_dry_days'] = dry_days.groupby((dry_days != dry_days.shift()).cumsum()).cumsum()
        
        print(f"Created water stress features. New shape: {df.shape}")
        return df
        
    def create_advanced_aggregations(self, df, groupby_cols=None, agg_cols=None):
        """
        Create advanced aggregation features
        
        Args:
            df: DataFrame with data
            groupby_cols: columns to group by (e.g., ['Area', 'Item'])
            agg_cols: columns to aggregate (e.g., ['rainfall', 'temperature_avg'])
        
        Returns:
            DataFrame with aggregation features
        """
        print("Creating advanced aggregation features...")
        
        if groupby_cols is None:
            groupby_cols = ['Area', 'Item'] if all(col in df.columns for col in ['Area', 'Item']) else []
        
        if agg_cols is None:
            agg_cols = ['rainfall', 'temperature_avg', 'yield_value']
            agg_cols = [col for col in agg_cols if col in df.columns]
        
        if groupby_cols and agg_cols:
            for group_col in groupby_cols:
                for agg_col in agg_cols:
                    if group_col in df.columns and agg_col in df.columns:
                        # Create group statistics
                        group_stats = df.groupby(group_col)[agg_col].agg(['mean', 'std', 'min', 'max'])
                        group_stats.columns = [f'{group_col}_{agg_col}_{stat}' for stat in ['mean', 'std', 'min', 'max']]
                        
                        # Reset index to make group_col a column for merging
                        group_stats = group_stats.reset_index()
                        
                        # Merge back to original dataframe
                        df = df.merge(group_stats, on=group_col, how='left')
                        
                        # Create relative features (value vs group average)
                        mean_col = f'{group_col}_{agg_col}_mean'
                        if mean_col in df.columns:
                            df[f'{agg_col}_vs_{group_col}_mean'] = df[agg_col] / (df[mean_col] + 1e-6)
        
        print(f"Created aggregation features. New shape: {df.shape}")
        return df
    
    def create_yield_stability_features(self, df):
        """
        Create features related to yield stability and trends
        
        Args:
            df: DataFrame with historical yield data
        
        Returns:
            DataFrame with yield stability features
        """
        print("Creating yield stability features...")
        
        if 'yield_value' in df.columns and 'year' in df.columns:
            # Sort by area, item, and year for proper calculation
            sort_cols = ['Area', 'Item', 'year'] if all(col in df.columns for col in ['Area', 'Item']) else ['year']
            df_sorted = df.sort_values(sort_cols)
            
            # Calculate yield trends and stability
            if all(col in df.columns for col in ['Area', 'Item']):
                # Group by Area and Item
                for group in ['Area', 'Item']:
                    if group in df.columns:
                        # Calculate rolling statistics for yield
                        df[f'yield_trend_{group.lower()}'] = df.groupby(group)['yield_value'].pct_change()
                        df[f'yield_volatility_{group.lower()}'] = df.groupby(group)['yield_value'].rolling(window=3, min_periods=1).std().reset_index(level=0, drop=True)
                        
                        # Years since highest/lowest yield
                        df[f'years_since_max_yield_{group.lower()}'] = df.groupby(group).apply(
                            lambda x: x['year'] - x.loc[x['yield_value'].idxmax(), 'year'] if len(x) > 0 else 0
                        ).reset_index(level=0, drop=True)
            else:
                # Global calculations if no grouping available
                df['yield_trend_global'] = df['yield_value'].pct_change()
                df['yield_volatility_global'] = df['yield_value'].rolling(window=3, min_periods=1).std()
        
        print(f"Created yield stability features. New shape: {df.shape}")
        return df
    
    def create_economic_features(self, df):
        """
        Create economic and efficiency-related features
        
        Args:
            df: DataFrame with economic data
        
        Returns:
            DataFrame with economic features
        """
        print("Creating economic features...")
        
        # Pesticide efficiency
        if 'pesticides_tonnes' in df.columns and 'yield_value' in df.columns:
            df['pesticide_efficiency'] = df['yield_value'] / (df['pesticides_tonnes'] + 1e-6)
            df['pesticide_intensity'] = df['pesticides_tonnes'] / (df['yield_value'] + 1e-6)
        
        # Resource utilization
        if all(col in df.columns for col in ['rainfall', 'yield_value']):
            df['water_use_efficiency'] = df['yield_value'] / (df['rainfall'] + 1e-6)
        
        if all(col in df.columns for col in ['nitrogen', 'yield_value']):
            df['nitrogen_use_efficiency'] = df['yield_value'] / (df['nitrogen'] + 1e-6)
        
        # Cost-benefit indicators
        if all(col in df.columns for col in ['pesticides_tonnes', 'nitrogen', 'phosphorus', 'potassium']):
            df['total_input_cost_proxy'] = df['pesticides_tonnes'] + df['nitrogen'] + df['phosphorus'] + df['potassium']
            if 'yield_value' in df.columns:
                df['input_output_ratio'] = df['yield_value'] / (df['total_input_cost_proxy'] + 1e-6)
        
        print(f"Created economic features. New shape: {df.shape}")
        return df
    
    def create_seasonal_patterns(self, df):
        """
        Create advanced seasonal pattern features
        
        Args:
            df: DataFrame with temporal data
        
        Returns:
            DataFrame with seasonal pattern features
        """
        print("Creating seasonal pattern features...")
        
        if 'month' in df.columns:
            # Advanced seasonal indicators
            df['is_peak_growing_season'] = ((df['month'] >= 4) & (df['month'] <= 7)).astype(int)  # April-July
            df['is_harvest_season'] = ((df['month'] >= 8) & (df['month'] <= 10)).astype(int)  # Aug-Oct
            df['is_winter_season'] = ((df['month'] == 12) | (df['month'] <= 2)).astype(int)  # Dec-Feb
            
            # Photoperiod approximation (day length)
            if 'latitude' in df.columns:
                # Simplified day length calculation
                day_of_year = df.get('day_of_year', 180)  # Default to mid-year if not available
                declination = 23.45 * np.sin(np.radians(360 * (284 + day_of_year) / 365))
                hour_angle = np.arccos(-np.tan(np.radians(df['latitude'])) * np.tan(np.radians(declination)))
                df['daylight_hours'] = 2 * hour_angle * 24 / (2 * np.pi)
                df['daylight_hours'] = np.clip(df['daylight_hours'], 0, 24)  # Ensure valid range
        
        if 'year' in df.columns:
            # Climate cycles (El Niño/La Niña approximation)
            df['el_nino_cycle'] = np.sin(2 * np.pi * (df['year'] % 7) / 7)  # ~7 year cycle
            df['decadal_climate_cycle'] = np.sin(2 * np.pi * (df['year'] % 11) / 11)  # ~11 year solar cycle
        
        print(f"Created seasonal pattern features. New shape: {df.shape}")
        return df
    
    def create_extreme_event_features(self, df):
        """
        Create features related to extreme weather events
        
        Args:
            df: DataFrame with weather data
        
        Returns:
            DataFrame with extreme event features
        """
        print("Creating extreme event features...")
        
        # Temperature extremes
        if 'temperature_max' in df.columns:
            # Heat wave indicators
            df['extreme_heat_days'] = (df['temperature_max'] > 40).astype(int)  # >40°C
            df['very_hot_days'] = (df['temperature_max'] > 35).astype(int)  # >35°C
            
        if 'temperature_min' in df.columns:
            # Cold stress indicators  
            df['frost_days'] = (df['temperature_min'] < 0).astype(int)
            df['severe_frost_days'] = (df['temperature_min'] < -5).astype(int)
            
        # Precipitation extremes
        if 'rainfall' in df.columns:
            # Define percentiles for extreme events
            rainfall_95th = df['rainfall'].quantile(0.95)
            rainfall_5th = df['rainfall'].quantile(0.05)
            
            df['extreme_rainfall_event'] = (df['rainfall'] > rainfall_95th).astype(int)
            df['drought_event'] = (df['rainfall'] < rainfall_5th).astype(int)
            df['moderate_drought'] = (df['rainfall'] < df['rainfall'].quantile(0.25)).astype(int)
            
            # Rainfall variability
            if len(df) > 7:
                df['rainfall_cv'] = df['rainfall'].rolling(window=7, min_periods=1).apply(
                    lambda x: x.std() / (x.mean() + 1e-6), raw=True
                )
        
        print(f"Created extreme event features. New shape: {df.shape}")
        return df


def select_important_features(df, target_column, method='correlation', top_k=20):
    """
    Select most important features for modeling
    
    Args:
        df: DataFrame with features and target
        target_column: name of target variable
        method: 'correlation', 'mutual_info', 'variance', or 'all'
        top_k: number of top features to select
    
    Returns:
        List of selected feature names or dict if method='all'
    """
    print(f"Selecting top {top_k} features using {method} method...")
    
    # Ensure target column exists
    if target_column not in df.columns:
        print(f"Warning: Target column '{target_column}' not found. Available columns: {list(df.columns)}")
        return []
    
    features = df.drop(columns=[target_column])
    target = df[target_column]
    
    # Remove non-numeric columns for feature selection
    numeric_features = features.select_dtypes(include=[np.number])
    
    if len(numeric_features.columns) == 0:
        print("Warning: No numeric features found for selection")
        return []
    
    if method == 'correlation':
        # Calculate correlation with target
        correlations = numeric_features.corrwith(target).abs().sort_values(ascending=False)
        correlations = correlations.dropna()  # Remove NaN correlations
        selected_features = correlations.head(min(top_k, len(correlations))).index.tolist()
        
    elif method == 'mutual_info':
        if not SKLEARN_AVAILABLE:
            print("Warning: scikit-learn not available. Cannot use mutual_info method.")
            return []
        
        # Handle NaN values
        clean_features = numeric_features.fillna(numeric_features.median())
        clean_target = target.fillna(target.median())
        
        mutual_info_regression = _get_mutual_info_regression()
        mi_scores = mutual_info_regression(clean_features, clean_target, random_state=42)
        mi_df = pd.DataFrame({'feature': clean_features.columns, 'score': mi_scores})
        selected_features = mi_df.nlargest(min(top_k, len(mi_df)), 'score')['feature'].tolist()
        
    elif method == 'variance':
        if not SKLEARN_AVAILABLE:
            print("Warning: scikit-learn not available. Cannot use variance method.")
            return []
        
        # Fill NaN values for variance calculation
        clean_features = numeric_features.fillna(numeric_features.median())
        
        VarianceThreshold = _get_variance_threshold()
        selector = VarianceThreshold(threshold=0.01)  # Remove very low variance features
        selector.fit(clean_features)
        high_var_features = clean_features.columns[selector.get_support()]
        selected_features = high_var_features[:min(top_k, len(high_var_features))].tolist()
        
    elif method == 'all':
        # Return results from all methods
        results = {}
        for m in ['correlation', 'mutual_info', 'variance']:
            try:
                results[m] = select_important_features(df, target_column, method=m, top_k=top_k)
            except Exception as e:
                print(f"Error in {m} method: {e}")
                results[m] = []
        return results
        
    else:
        raise ValueError(f"Unknown method: {method}. Use 'correlation', 'mutual_info', 'variance', or 'all'")
    
    print(f"Selected {len(selected_features)} features using {method} method:")
    for i, feature in enumerate(selected_features[:10]):  # Show top 10
        print(f"  {i+1}. {feature}")
    if len(selected_features) > 10:
        print(f"  ... and {len(selected_features) - 10} more")
    
    return selected_features


def create_feature_summary(df, target_column=None):
    """
    Create a comprehensive summary of features in the dataset
    
    Args:
        df: DataFrame to analyze
        target_column: name of target variable (optional)
    
    Returns:
        Dictionary with feature summary information
    """
    print("Creating feature summary...")
    
    summary = {
        'total_features': len(df.columns),
        'numeric_features': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_features': len(df.select_dtypes(include=['object', 'category']).columns),
        'datetime_features': len(df.select_dtypes(include=['datetime64']).columns),
        'missing_values': df.isnull().sum().sum(),
        'rows': len(df),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
    }
    
    # Feature types breakdown
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        summary['numeric_stats'] = {
            'mean_values': df[numeric_cols].mean().to_dict(),
            'std_values': df[numeric_cols].std().to_dict(),
            'min_values': df[numeric_cols].min().to_dict(),
            'max_values': df[numeric_cols].max().to_dict()
        }
    
    # Missing values by column
    missing_by_col = df.isnull().sum()
    summary['missing_by_column'] = missing_by_col[missing_by_col > 0].to_dict()
    
    # Correlation with target if provided
    if target_column and target_column in df.columns:
        correlations = df[numeric_cols].corrwith(df[target_column]).abs().sort_values(ascending=False)
        summary['target_correlations'] = correlations.dropna().head(10).to_dict()
    
    print(f"Feature summary created:")
    print(f"  Total features: {summary['total_features']}")
    print(f"  Numeric: {summary['numeric_features']}, Categorical: {summary['categorical_features']}")
    print(f"  Missing values: {summary['missing_values']} ({summary['missing_values']/(len(df)*len(df.columns))*100:.2f}%)")
    print(f"  Memory usage: {summary['memory_usage_mb']:.2f} MB")
    
    return summary


def detect_feature_types(df):
    """
    Automatically detect and categorize feature types
    
    Args:
        df: DataFrame to analyze
    
    Returns:
        Dictionary with categorized feature lists
    """
    feature_types = {
        'numeric_continuous': [],
        'numeric_discrete': [],
        'categorical_nominal': [],
        'categorical_ordinal': [],
        'datetime': [],
        'text': [],
        'binary': [],
        'id_columns': []
    }
    
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            # Check if it's binary (0/1 or similar)
            unique_vals = df[col].dropna().unique()
            if len(unique_vals) == 2:
                feature_types['binary'].append(col)
            elif len(unique_vals) < 10 and df[col].dtype == 'int64':
                feature_types['numeric_discrete'].append(col)
            else:
                feature_types['numeric_continuous'].append(col)
                
        elif df[col].dtype == 'object':
            unique_count = df[col].nunique()
            if unique_count == len(df):  # Likely ID column
                feature_types['id_columns'].append(col)
            elif unique_count < 20:  # Likely categorical
                feature_types['categorical_nominal'].append(col)
            else:  # Likely text
                feature_types['text'].append(col)
                
        elif df[col].dtype.name.startswith('datetime'):
            feature_types['datetime'].append(col)
    
    print("Feature types detected:")
    for ftype, cols in feature_types.items():
        if cols:
            print(f"  {ftype}: {len(cols)} features")
    
    return feature_types


if __name__ == "__main__":
    print("=" * 60)
    print("Feature Engineering Utilities for Crop Yield Prediction")
    print("=" * 60)
    print("\nAvailable Classes and Functions:")
    print("\n1. FeatureEngineer Class:")
    print("   - create_weather_features()     : Weather-based features")
    print("   - create_soil_features()        : Soil nutrient features")
    print("   - create_ndvi_features()        : Vegetation health features")
    print("   - create_geographic_features()  : Location-based features")
    print("   - create_temporal_features()    : Time-based features")
    print("   - create_climate_features()     : Climate indices")
    print("   - create_water_stress_features(): Water stress indicators")
    print("   - create_advanced_aggregations(): Group-based statistical features")
    print("   - create_economic_features()    : Resource efficiency indicators")
    print("   - create_seasonal_patterns()    : Advanced seasonal features")
    print("   - create_extreme_event_features(): Extreme weather detection")
    print("   - create_yield_stability_features(): Yield trends and stability")
    print("   - create_interaction_features() : Feature interactions")
    print("   - create_polynomial_features()  : Polynomial transformations")
    print("   - feature_engineering_pipeline(): Complete pipeline")
    print("\n2. Utility Functions:")
    print("   - select_important_features()   : Feature selection")
    print("   - create_feature_summary()      : Dataset analysis")
    print("   - detect_feature_types()        : Automatic type detection")
    
    print("\n" + "="*60)
    print("Example Usage:")
    print("""\nfrom utils.feature_engineering import FeatureEngineer

# Initialize feature engineer
fe = FeatureEngineer()

# Load your data
df = pd.read_csv('your_data.csv')

# Apply complete feature engineering
enhanced_df = fe.feature_engineering_pipeline(
    df, 
    include_interactions=True,
    include_climate=True,
    include_water_stress=True
)

# Select important features
from utils.feature_engineering import select_important_features
top_features = select_important_features(
    enhanced_df, 
    target_column='yield_value',
    method='correlation',
    top_k=20
)""")
    print("\n" + "="*60)
    print("Import this module to use feature engineering functions")
    print("For detailed documentation, check individual function docstrings")
    print("=" * 60)