"""
Data Preprocessing Utilities for Crop Yield Prediction

This module contains functions for data cleaning, preprocessing, and preparation
for machine learning models.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import packages with proper error handling to avoid linter issues
import importlib
from typing import Any, Optional, Dict, List, Tuple, Union

# Module availability flags
SKLEARN_AVAILABLE = False
SCIPY_AVAILABLE = False

# Import sklearn with error handling
try:
    sklearn_preprocessing = importlib.import_module('sklearn.preprocessing')
    sklearn_impute = importlib.import_module('sklearn.impute')
    SKLEARN_AVAILABLE = True
except ImportError:
    print("Warning: scikit-learn not available. Some preprocessing features may not work.")
    print("Install with: pip install scikit-learn")
    SKLEARN_AVAILABLE = False
    
    # Create fallback classes
    class _DummyScaler:
        def fit_transform(self, X):
            return X
        def transform(self, X):
            return X
        def fit(self, X):
            return self
    
    class _DummyImputer:
        def __init__(self, strategy='mean'):
            self.strategy = strategy
        def fit_transform(self, X):
            return X
        def transform(self, X):
            return X
        def fit(self, X):
            return self
    
    class _DummyEncoder:
        def __init__(self):
            self.classes_ = []
        def fit_transform(self, X):
            return np.arange(len(X))
        def transform(self, X):
            return np.arange(len(X))
        def fit(self, X):
            return self

# Import scipy with error handling
try:
    scipy_stats = importlib.import_module('scipy.stats')
    SCIPY_AVAILABLE = True
except ImportError:
    print("Warning: scipy not available. Some statistical features may not work.")
    print("Install with: pip install scipy")
    SCIPY_AVAILABLE = False

# Helper functions to get the right classes
def _get_standard_scaler():
    if SKLEARN_AVAILABLE:
        return sklearn_preprocessing.StandardScaler
    else:
        return _DummyScaler

def _get_minmax_scaler():
    if SKLEARN_AVAILABLE:
        return sklearn_preprocessing.MinMaxScaler
    else:
        return _DummyScaler

def _get_robust_scaler():
    if SKLEARN_AVAILABLE:
        return sklearn_preprocessing.RobustScaler
    else:
        return _DummyScaler

def _get_label_encoder():
    if SKLEARN_AVAILABLE:
        return sklearn_preprocessing.LabelEncoder
    else:
        return _DummyEncoder

def _get_simple_imputer():
    if SKLEARN_AVAILABLE:
        return sklearn_impute.SimpleImputer
    else:
        return _DummyImputer


class DataPreprocessor:
    """
    A comprehensive data preprocessing class for crop yield prediction
    """
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        
    def handle_missing_values(self, df, strategy='mean', threshold=0.5):
        """
        Handle missing values in the dataset
        
        Args:
            df: pandas DataFrame
            strategy: 'mean', 'median', 'mode', 'drop', or 'interpolate'
            threshold: drop columns with missing values > threshold
        
        Returns:
            Cleaned DataFrame
        """
        print(f"Original shape: {df.shape}")
        
        # Check missing values
        missing_info = df.isnull().sum()
        missing_percent = (missing_info / len(df)) * 100
        
        print("\nMissing values summary:")
        for col, pct in missing_percent.items():
            if pct > 0:
                print(f"  {col}: {pct:.2f}%")
        
        # Drop columns with too many missing values
        cols_to_drop = missing_percent[missing_percent > threshold * 100].index
        if len(cols_to_drop) > 0:
            print(f"\nDropping columns with >{threshold*100}% missing: {list(cols_to_drop)}")
            df = df.drop(columns=cols_to_drop)
        
        # Handle remaining missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        if strategy == 'mean':
            SimpleImputer = _get_simple_imputer()
            imputer = SimpleImputer(strategy='mean')
            df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
            self.imputers['numeric'] = imputer
            
        elif strategy == 'median':
            SimpleImputer = _get_simple_imputer()
            imputer = SimpleImputer(strategy='median')
            df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
            self.imputers['numeric'] = imputer
            
        elif strategy == 'interpolate':
            for col in numeric_cols:
                df[col] = df[col].interpolate()
        
        # Handle categorical missing values
        if len(categorical_cols) > 0:
            SimpleImputer = _get_simple_imputer()
            cat_imputer = SimpleImputer(strategy='most_frequent')
            df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])
            self.imputers['categorical'] = cat_imputer
        
        print(f"After preprocessing shape: {df.shape}")
        return df
    
    def remove_outliers(self, df, columns=None, method='iqr', factor=1.5):
        """
        Remove outliers from specified columns
        
        Args:
            df: pandas DataFrame
            columns: list of columns to check for outliers (None = all numeric)
            method: 'iqr' or 'zscore'
            factor: multiplier for IQR method or threshold for z-score
        
        Returns:
            DataFrame with outliers removed
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        original_len = len(df)
        
        for col in columns:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - factor * IQR
                upper_bound = Q3 + factor * IQR
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
                
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                df = df[z_scores < factor]
        
        removed_count = original_len - len(df)
        print(f"Removed {removed_count} outliers ({removed_count/original_len*100:.2f}%)")
        
        return df
    
    def encode_categorical_variables(self, df, columns=None):
        """
        Encode categorical variables
        
        Args:
            df: pandas DataFrame
            columns: list of categorical columns (None = auto-detect)
        
        Returns:
            DataFrame with encoded categorical variables
        """
        if columns is None:
            columns = df.select_dtypes(include=['object']).columns
        
        for col in columns:
            LabelEncoder = _get_label_encoder()
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col].astype(str))
            self.encoders[col] = encoder
            print(f"Encoded {col}: {len(getattr(encoder, 'classes_', []))} categories")
        
        return df
    
    def scale_features(self, df, columns=None, method='standard'):
        """
        Scale numerical features
        
        Args:
            df: pandas DataFrame
            columns: list of columns to scale (None = all numeric)
            method: 'standard', 'minmax', or 'robust'
        
        Returns:
            DataFrame with scaled features
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        if method == 'standard':
            StandardScaler = _get_standard_scaler()
            scaler = StandardScaler()
        elif method == 'minmax':
            MinMaxScaler = _get_minmax_scaler()
            scaler = MinMaxScaler()
        else:
            RobustScaler = _get_robust_scaler()
            scaler = RobustScaler()
        
        df[columns] = scaler.fit_transform(df[columns])
        self.scalers[method] = scaler
        
        print(f"Scaled {len(columns)} columns using {method} scaling")
        return df
    
    def create_date_features(self, df, date_column):
        """
        Extract features from date column
        
        Args:
            df: pandas DataFrame
            date_column: name of date column
        
        Returns:
            DataFrame with date features added
        """
        df[date_column] = pd.to_datetime(df[date_column])
        
        df['year'] = df[date_column].dt.year
        df['month'] = df[date_column].dt.month
        df['day_of_year'] = df[date_column].dt.dayofyear
        df['quarter'] = df[date_column].dt.quarter
        df['season'] = df['month'].apply(self._get_season)
        
        print(f"Created date features from {date_column}")
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
    
    def detect_outliers(self, df: pd.DataFrame, columns: Optional[List[str]] = None, 
                       methods: List[str] = ['iqr'], return_indices: bool = False):
        """
        Detect outliers using multiple methods
        
        Args:
            df: pandas DataFrame
            columns: list of columns to check (None = all numeric)
            methods: list of outlier detection methods
            return_indices: if True, return outlier indices
        
        Returns:
            DataFrame with outliers removed or list of outlier indices
        """
        if columns is None:
            columns = list(df.select_dtypes(include=[np.number]).columns)
        
        outlier_indices = set()
        outlier_report = {}
        
        for col in columns:
            col_outliers = set()
            
            if 'iqr' in methods:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                iqr_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index
                col_outliers.update(iqr_outliers)
            
            if 'zscore' in methods:
                if SCIPY_AVAILABLE:
                    z_scores = np.abs(scipy_stats.zscore(df[col].dropna()))
                    zscore_outliers = df[col].dropna().iloc[z_scores > 3].index
                    col_outliers.update(zscore_outliers)
                else:
                    print(f"Warning: scipy not available, skipping z-score outlier detection for {col}")
            
            outlier_indices.update(col_outliers)
            outlier_report[col] = len(col_outliers)
        
        print(f"Outlier detection summary:")
        for col, count in outlier_report.items():
            if count > 0:
                print(f"  {col}: {count} outliers ({count/len(df)*100:.2f}%)")
        
        if return_indices:
            return list(outlier_indices)
        else:
            clean_df = df.drop(index=list(outlier_indices)) if outlier_indices else df
            print(f"Removed {len(outlier_indices)} outlier rows")
            return clean_df
    
    def handle_duplicates(self, df, subset=None, keep='first'):
        """
        Handle duplicate rows in the dataset
        
        Args:
            df: pandas DataFrame
            subset: columns to consider for duplicate detection
            keep: which duplicate to keep ('first', 'last', False)
        
        Returns:
            DataFrame with duplicates handled
        """
        original_len = len(df)
        duplicate_count = df.duplicated(subset=subset, keep=False).sum()
        
        if duplicate_count > 0:
            print(f"Found {duplicate_count} duplicate rows ({duplicate_count/original_len*100:.2f}%)")
            df = df.drop_duplicates(subset=subset, keep=keep)
            print(f"Removed {original_len - len(df)} duplicate rows")
        else:
            print("No duplicate rows found")
        
        return df
    
    def normalize_column_names(self, df):
        """
        Normalize column names for consistency
        
        Args:
            df: pandas DataFrame
        
        Returns:
            DataFrame with normalized column names
        """
        original_columns = df.columns.tolist()
        
        # Strip whitespace and normalize case
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Remove special characters
        df.columns = df.columns.str.replace(r'[^a-zA-Z0-9_]', '', regex=True)
        
        # Ensure columns start with letter
        df.columns = [f"col_{col}" if col[0].isdigit() else col for col in df.columns]
        
        changes = [(orig, new) for orig, new in zip(original_columns, df.columns) if orig != new]
        if changes:
            print("Column name changes:")
            for orig, new in changes:
                print(f"  '{orig}' -> '{new}'")
        
        return df
    
    def handle_data_types(self, df, optimize_memory=True):
        """
        Optimize data types for memory efficiency and performance
        
        Args:
            df: pandas DataFrame
            optimize_memory: whether to optimize for memory usage
        
        Returns:
            DataFrame with optimized data types
        """
        print("Optimizing data types...")
        memory_before = df.memory_usage(deep=True).sum() / 1024**2
        
        for col in df.columns:
            col_type = df[col].dtype
            
            # Optimize integer columns
            if col_type == 'int64':
                if df[col].min() >= 0 and df[col].max() <= 255:
                    df[col] = df[col].astype('uint8')
                elif df[col].min() >= -128 and df[col].max() <= 127:
                    df[col] = df[col].astype('int8')
                elif df[col].min() >= -32768 and df[col].max() <= 32767:
                    df[col] = df[col].astype('int16')
                elif df[col].min() >= -2147483648 and df[col].max() <= 2147483647:
                    df[col] = df[col].astype('int32')
            
            # Optimize float columns
            elif col_type == 'float64':
                if df[col].min() >= np.finfo(np.float32).min and df[col].max() <= np.finfo(np.float32).max:
                    df[col] = df[col].astype('float32')
            
            # Convert object columns with few unique values to category
            elif col_type == 'object' and optimize_memory:
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.5:  # Less than 50% unique values
                    df[col] = df[col].astype('category')
                    print(f"Converted {col} to category (unique ratio: {unique_ratio:.2f})")
        
        memory_after = df.memory_usage(deep=True).sum() / 1024**2
        memory_reduction = ((memory_before - memory_after) / memory_before) * 100
        
        print(f"Memory usage reduced by {memory_reduction:.1f}% ({memory_before:.1f}MB -> {memory_after:.1f}MB)")
        return df
    
    def create_bins(self, df, columns=None, n_bins=5, strategy='quantile'):
        """
        Create bins for continuous variables
        
        Args:
            df: pandas DataFrame
            columns: columns to bin (None = all numeric with high cardinality)
            n_bins: number of bins to create
            strategy: 'quantile', 'uniform', or 'kmeans'
        
        Returns:
            DataFrame with binned features
        """
        if columns is None:
            # Auto-select numeric columns with high cardinality
            columns = [col for col in df.select_dtypes(include=[np.number]).columns 
                      if df[col].nunique() > 20]
        
        for col in columns:
            if col not in df.columns:
                continue
            
            try:
                if strategy == 'quantile':
                    df[f"{col}_binned"] = pd.qcut(df[col], q=n_bins, labels=False, duplicates='drop')
                elif strategy == 'uniform':
                    df[f"{col}_binned"] = pd.cut(df[col], bins=n_bins, labels=False)
                elif strategy == 'kmeans' and SKLEARN_AVAILABLE:
                    try:
                        sklearn_cluster = importlib.import_module('sklearn.cluster') 
                        KMeans = sklearn_cluster.KMeans
                        kmeans = KMeans(n_clusters=n_bins, random_state=42, n_init=10)
                        df[f"{col}_binned"] = kmeans.fit_predict(df[[col]])
                    except ImportError:
                        print(f"Warning: sklearn.cluster not available, using uniform binning for {col}")
                        df[f"{col}_binned"] = pd.cut(df[col], bins=n_bins, labels=False)
                else:
                    # Fallback to uniform if sklearn not available
                    df[f"{col}_binned"] = pd.cut(df[col], bins=n_bins, labels=False)
                
                print(f"Created {n_bins} bins for {col} using {strategy} strategy")
                
            except Exception as e:
                print(f"Warning: Could not bin {col}: {str(e)}")
                continue
        
        return df
    
    def transform_distributions(self, df, columns=None, method='log'):
        """
        Transform skewed distributions to more normal distributions
        
        Args:
            df: pandas DataFrame
            columns: columns to transform (None = auto-detect skewed columns)
            method: 'log', 'sqrt', 'boxcox', 'yeo-johnson'
        
        Returns:
            DataFrame with transformed distributions
        """
        if columns is None:
            # Auto-detect highly skewed numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            columns = []
            
            for col in numeric_cols:
                if df[col].nunique() > 10:  # Skip low-cardinality columns
                    skewness = df[col].skew()
                    if abs(skewness) > 1:  # Highly skewed
                        columns.append(col)
                        print(f"Detected skewed column {col} (skewness: {skewness:.2f})")
        
        for col in columns:
            if col not in df.columns:
                continue
            
            try:
                original_col = df[col].copy()
                
                if method == 'log':
                    # Add small constant to handle zeros/negatives
                    min_val = df[col].min()
                    if min_val <= 0:
                        shift = abs(min_val) + 1
                        df[f"{col}_log"] = np.log(df[col] + shift)
                    else:
                        df[f"{col}_log"] = np.log(df[col])
                    
                elif method == 'sqrt':
                    # Handle negative values
                    if df[col].min() < 0:
                        df[f"{col}_sqrt"] = np.sign(df[col]) * np.sqrt(np.abs(df[col]))
                    else:
                        df[f"{col}_sqrt"] = np.sqrt(df[col])
                
                elif method == 'boxcox' and SCIPY_AVAILABLE:
                    if df[col].min() > 0:  # Box-Cox requires positive values
                        transformed, lambda_param = scipy_stats.boxcox(df[col])
                        df[f"{col}_boxcox"] = transformed
                        print(f"Applied Box-Cox to {col} (λ={lambda_param:.3f})")
                    else:
                        print(f"Skipped Box-Cox for {col} (contains non-positive values)")
                        continue
                
                elif method == 'yeo-johnson' and SCIPY_AVAILABLE:
                    transformed, lambda_param = scipy_stats.yeojohnson(df[col])
                    df[f"{col}_yeojohnson"] = transformed
                    print(f"Applied Yeo-Johnson to {col} (λ={lambda_param:.3f})")
                
                # Calculate skewness improvement
                if method in ['log', 'sqrt'] or (method in ['boxcox', 'yeo-johnson'] and SCIPY_AVAILABLE):
                    new_col = f"{col}_{method}"
                    if new_col in df.columns:
                        original_skew = original_col.skew()
                        new_skew = df[new_col].skew()
                        improvement = abs(original_skew) - abs(new_skew)
                        print(f"Transformed {col}: skewness {original_skew:.2f} -> {new_skew:.2f} (improvement: {improvement:.2f})")
                
            except Exception as e:
                print(f"Warning: Could not transform {col}: {str(e)}")
                continue
        
        return df
    
    def advanced_encoding(self, df, columns=None, method='onehot'):
        """
        Advanced categorical encoding methods
        
        Args:
            df: pandas DataFrame
            columns: columns to encode (None = all categorical)
            method: 'onehot', 'label'
        
        Returns:
            DataFrame with encoded variables
        """
        if columns is None:
            columns = df.select_dtypes(include=['object', 'category']).columns
        
        for col in columns:
            if col not in df.columns:
                continue
                
            if method == 'onehot':
                # Simple one-hot encoding using pandas
                dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
                df = pd.concat([df.drop(columns=[col]), dummies], axis=1)
                print(f"One-hot encoded {col}: {len(dummies.columns)} new features")
                
            elif method == 'label':
                LabelEncoder = _get_label_encoder()
                encoder = LabelEncoder()
                df[col] = encoder.fit_transform(df[col].astype(str))
                self.encoders[f"{col}_label"] = encoder
                print(f"Label encoded {col}: {len(getattr(encoder, 'classes_', []))} categories")
        
        return df
    
    def preprocess_pipeline(self, df: pd.DataFrame, target_column: Optional[str] = None, 
                          missing_strategy: str = 'mean',
                          remove_outliers_flag: bool = True,
                          scale_method: str = 'standard',
                          encoding_method: str = 'label',
                          handle_duplicates_flag: bool = True,
                          normalize_names: bool = True,
                          optimize_dtypes: bool = True,
                          create_bins_flag: bool = False,
                          transform_skewed: bool = False) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Complete preprocessing pipeline with all steps
        
        Args:
            df: pandas DataFrame
            target_column: name of target variable
            missing_strategy: strategy for handling missing values
            remove_outliers_flag: whether to remove outliers
            scale_method: scaling method for features
            encoding_method: categorical encoding method
            handle_duplicates_flag: whether to handle duplicates
            normalize_names: whether to normalize column names
            optimize_dtypes: whether to optimize data types
            create_bins_flag: whether to create bins for continuous variables
            transform_skewed: whether to transform skewed distributions
        
        Returns:
            Preprocessed DataFrame and preprocessing report
        """
        print("Starting comprehensive preprocessing pipeline...")
        print(f"Input shape: {df.shape}")
        
        # Store original info for report
        original_shape = df.shape
        preprocessing_steps = []
        
        # Step 1: Normalize column names
        if normalize_names:
            df = self.normalize_column_names(df)
            preprocessing_steps.append("Column names normalized")
        
        # Step 2: Optimize data types
        if optimize_dtypes:
            df = self.handle_data_types(df)
            preprocessing_steps.append("Data types optimized")
        
        # Step 3: Handle duplicates
        if handle_duplicates_flag:
            df = self.handle_duplicates(df)
            preprocessing_steps.append("Duplicates handled")
        
        # Step 4: Handle missing values
        df = self.handle_missing_values(df, strategy=missing_strategy)
        preprocessing_steps.append(f"Missing values handled ({missing_strategy})")
        
        # Step 5: Transform skewed distributions (before outlier removal)
        if transform_skewed:
            df = self.transform_distributions(df, method='log')
            preprocessing_steps.append("Skewed distributions transformed")
        
        # Step 6: Create bins for continuous variables
        if create_bins_flag:
            df = self.create_bins(df, strategy='quantile')
            preprocessing_steps.append("Continuous variables binned")
        
        # Step 7: Remove outliers (except for target variable)
        if remove_outliers_flag:
            exclude_cols = [target_column] if target_column else []
            outlier_cols = [col for col in df.select_dtypes(include=[np.number]).columns 
                           if col not in exclude_cols]
            if outlier_cols:
                # Use type assertion to tell type checker this returns a DataFrame
                outlier_result = self.detect_outliers(df, columns=outlier_cols, return_indices=False)
                if isinstance(outlier_result, pd.DataFrame):
                    df = outlier_result
                preprocessing_steps.append("Outliers removed")
        
        # Step 8: Encode categorical variables
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            df = self.advanced_encoding(df, method=encoding_method)
            preprocessing_steps.append(f"Categorical variables encoded ({encoding_method})")
        
        # Step 9: Scale features (except target variable)
        if target_column and target_column in df.columns:
            feature_cols = [col for col in df.select_dtypes(include=[np.number]).columns 
                           if col != target_column]
        else:
            feature_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(feature_cols) > 0:
            df = self.scale_features(df, columns=feature_cols, method=scale_method)
            preprocessing_steps.append(f"Features scaled ({scale_method})")
        
        # Generate preprocessing report
        report = {
            'original_shape': original_shape,
            'final_shape': df.shape,
            'rows_removed': original_shape[0] - df.shape[0],
            'columns_added': df.shape[1] - original_shape[1],
            'steps_completed': preprocessing_steps,
            'preprocessing_objects': {
                'scalers': list(self.scalers.keys()),
                'encoders': list(self.encoders.keys()),
                'imputers': list(self.imputers.keys())
            }
        }
        
        print("\nPreprocessing pipeline completed!")
        print(f"Final shape: {df.shape}")
        print(f"Rows removed: {report['rows_removed']}")
        print(f"Columns added: {report['columns_added']}")
        
        return df, report


def load_and_merge_datasets(data_paths: Dict[str, str]) -> pd.DataFrame:
    """
    Load multiple datasets and merge them
    
    Args:
        data_paths: dictionary with dataset names as keys and file paths as values
    
    Returns:
        Merged DataFrame
    """
    datasets = {}
    
    for name, path in data_paths.items():
        try:
            datasets[name] = pd.read_csv(path)
            print(f"Loaded {name}: {datasets[name].shape}")
        except FileNotFoundError:
            print(f"Warning: {path} not found, skipping {name}")
    
    # Initialize merged_data with empty DataFrame
    merged_data = pd.DataFrame()
    
    # Example merge logic - adjust based on your data structure
    if 'crop_yield' in datasets:
        merged_data = datasets['crop_yield']
        
        for name, df in datasets.items():
            if name != 'crop_yield' and 'location' in df.columns:
                merged_data = pd.merge(merged_data, df, on='location', how='left')
                print(f"Merged {name} data")
    elif datasets:  # If no 'crop_yield' but we have datasets
        # Use the first dataset as base
        first_key = list(datasets.keys())[0]
        merged_data = datasets[first_key]
        print(f"Using {first_key} as base dataset")
    
    if merged_data.empty:
        print("Warning: No data could be loaded or merged")
        
    return merged_data


def validate_data_quality(df, target_column=None):
    """
    Comprehensive data quality validation and reporting
    
    Args:
        df: pandas DataFrame
        target_column: name of target variable for additional analysis
    
    Returns:
        Dictionary with comprehensive data quality metrics
    """
    print("\n" + "="*50)
    print("COMPREHENSIVE DATA QUALITY REPORT")
    print("="*50)
    
    # Basic statistics
    basic_stats = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'duplicate_rows': df.duplicated().sum(),
    }
    
    # Missing values analysis
    missing_analysis = {
        'total_missing': df.isnull().sum().sum(),
        'missing_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
        'columns_with_missing': df.columns[df.isnull().any()].tolist(),
        'missing_by_column': df.isnull().sum().to_dict()
    }
    
    # Data type analysis
    type_analysis = {
        'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_columns': len(df.select_dtypes(include=['object', 'category']).columns),
        'column_types': df.dtypes.astype(str).to_dict()
    }
    
    # Uniqueness analysis
    uniqueness_analysis = {
        'unique_values_per_column': df.nunique().to_dict(),
        'potential_id_columns': [col for col in df.columns if df[col].nunique() == len(df)],
        'constant_columns': [col for col in df.columns if df[col].nunique() <= 1]
    }
    
    # Data quality score calculation
    quality_score = 100
    quality_issues = []
    
    # Deduct points for issues
    if missing_analysis['missing_percentage'] > 10:
        quality_score -= 20
        quality_issues.append(f"High missing values: {missing_analysis['missing_percentage']:.1f}%")
    
    if basic_stats['duplicate_rows'] > len(df) * 0.05:
        quality_score -= 15
        quality_issues.append(f"High duplicate rows: {basic_stats['duplicate_rows']}")
    
    if len(uniqueness_analysis['constant_columns']) > 0:
        quality_score -= 10
        quality_issues.append(f"Constant columns found: {len(uniqueness_analysis['constant_columns'])}")
    
    # Target variable analysis (if provided)
    target_analysis = {}
    if target_column and target_column in df.columns:
        target_series = df[target_column]
        target_analysis = {
            'target_type': str(target_series.dtype),
            'target_missing': target_series.isnull().sum(),
            'target_unique_values': target_series.nunique(),
            'target_statistics': target_series.describe().to_dict() if target_series.dtype in ['int64', 'float64'] else None
        }
    
    # Compile final report
    final_report = {
        'status': 'EXCELLENT' if quality_score >= 90 else 'GOOD' if quality_score >= 70 else 'NEEDS_ATTENTION',
        'quality_score': quality_score,
        'quality_issues': quality_issues,
        'basic_statistics': basic_stats,
        'missing_values': missing_analysis,
        'data_types': type_analysis,
        'uniqueness': uniqueness_analysis,
        'target_analysis': target_analysis if target_analysis else None
    }
    
    # Print summary
    print(f"\n📊 OVERALL QUALITY SCORE: {quality_score}/100 ({final_report['status']})")
    print(f"📋 Dataset Shape: {basic_stats['total_rows']} rows × {basic_stats['total_columns']} columns")
    print(f"💾 Memory Usage: {basic_stats['memory_usage_mb']:.2f} MB")
    print(f"❌ Missing Values: {missing_analysis['total_missing']} ({missing_analysis['missing_percentage']:.2f}%)")
    print(f"🔄 Duplicate Rows: {basic_stats['duplicate_rows']}")
    print(f"📈 Numeric Columns: {type_analysis['numeric_columns']}")
    print(f"📝 Categorical Columns: {type_analysis['categorical_columns']}")
    
    if quality_issues:
        print(f"\n⚠️  ISSUES DETECTED:")
        for issue in quality_issues:
            print(f"   • {issue}")
    
    print("="*50)
    
    return final_report


if __name__ == "__main__":
    print("=" * 60)
    print("Data Preprocessing Utilities for Crop Yield Prediction")
    print("=" * 60)
    print("\nAvailable Classes and Functions:")
    print("\n1. DataPreprocessor Class:")
    print("   - handle_missing_values()       : Smart missing value imputation")
    print("   - detect_outliers()             : Multi-method outlier detection")
    print("   - handle_duplicates()           : Duplicate row management")
    print("   - normalize_column_names()      : Column name standardization")
    print("   - handle_data_types()           : Data type optimization")
    print("   - create_bins()                 : Continuous to categorical binning")
    print("   - advanced_encoding()           : Multiple encoding methods")
    print("   - transform_distributions()     : Distribution normalization")
    print("   - preprocess_pipeline()         : Complete preprocessing workflow")
    print("\n2. Utility Functions:")
    print("   - load_and_merge_datasets()     : Intelligent dataset loading")
    print("   - validate_data_quality()       : Comprehensive quality assessment")
    
    print("\n" + "="*60)
    print("Example Usage:")
    print("""\nfrom utils.preprocessing import DataPreprocessor

# Initialize preprocessor
preprocessor = DataPreprocessor()

# Load your data
df = pd.read_csv('your_data.csv')

# Apply complete preprocessing
clean_df, report = preprocessor.preprocess_pipeline(
    df,
    target_column='yield_value',
    missing_strategy='median',
    encoding_method='onehot',
    scale_method='robust'
)

# Validate data quality
from utils.preprocessing import validate_data_quality
quality_report = validate_data_quality(clean_df, target_column='yield_value')""")
    print("\n" + "="*60)
    print("Import this module to use comprehensive preprocessing functions")
    print("For detailed documentation, check individual function docstrings")
    print("=" * 60)