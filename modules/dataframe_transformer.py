import pandas as pd
from typing import Dict, List, Union, Optional, Tuple, Any
import logging
from datetime import datetime

# Configure logger
logger = logging.getLogger(__name__)


def standardize_column_names(df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Standardize column names in a DataFrame based on a mapping or default rules.
    
    Args:
        df (pd.DataFrame): Input DataFrame with columns to standardize
        column_mapping (Optional[Dict[str, str]]): Optional mapping of original column names to standardized names
    
    Returns:
        pd.DataFrame: DataFrame with standardized column names
    """
    if df is None or df.empty:
        logger.warning("Empty DataFrame provided to standardize_column_names")
        return df
    
    # Create a copy to avoid modifying the original DataFrame
    result_df = df.copy()
    
    # If no mapping is provided, use default standardization rules
    if column_mapping is None:
        # Default standardization: lowercase, replace spaces with underscores
        result_df.columns = result_df.columns.str.strip().str.replace(' ', '_').str.lower()
        logger.debug(f"Applied default column name standardization: {list(result_df.columns)}")
    else:
        # Apply the provided mapping
        renamed_columns = {}
        for original, standardized in column_mapping.items():
            if original in result_df.columns:
                renamed_columns[original] = standardized
        
        if renamed_columns:
            result_df = result_df.rename(columns=renamed_columns)
            logger.debug(f"Applied custom column mapping: {renamed_columns}")
    
    return result_df

def standardize_time_format(df: pd.DataFrame, time_column: str = 'timestamp', 
                           format: Optional[str] = None) -> pd.DataFrame:
    """
    Standardize the time format in a DataFrame's timestamp column.
    
    Args:
        df (pd.DataFrame): Input DataFrame with timestamp column
        time_column (str): Name of the column containing timestamps
        format (Optional[str]): Optional datetime format string for parsing
    
    Returns:
        pd.DataFrame: DataFrame with standardized time format
    """
    if df is None or df.empty:
        logger.warning("Empty DataFrame provided to standardize_time_format")
        return df
    
    result_df = df.copy()
    
    # Check if the time column exists
    if time_column not in result_df.columns:
        logger.warning(f"Time column '{time_column}' not found in DataFrame. Available columns: {list(result_df.columns)}")
        return result_df
    
    try:
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(result_df[time_column]):
            if format:
                result_df[time_column] = pd.to_datetime(result_df[time_column], format=format, errors='coerce')
            else:
                result_df[time_column] = pd.to_datetime(result_df[time_column], errors='coerce')
            
            # Check for NaT values after conversion
            nat_count = result_df[time_column].isna().sum()
            if nat_count > 0:
                logger.warning(f"Conversion to datetime resulted in {nat_count} NaT values in column '{time_column}'")
            else:
                logger.debug(f"Successfully converted column '{time_column}' to datetime")
    except Exception as e:
        logger.error(f"Error converting column '{time_column}' to datetime: {str(e)}")
    
    return result_df

def ensure_numeric_columns(df: pd.DataFrame, numeric_columns: List[str]) -> pd.DataFrame:
    """
    Ensure specified columns are of numeric type.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        numeric_columns (List[str]): List of column names that should be numeric
    
    Returns:
        pd.DataFrame: DataFrame with numeric columns converted
    """
    if df is None or df.empty:
        logger.warning("Empty DataFrame provided to ensure_numeric_columns")
        return df
    
    result_df = df.copy()
    
    for col in numeric_columns:
        if col in result_df.columns:
            try:
                # Store original values for comparison
                original_values = result_df[col].copy()
                
                # Convert to numeric
                result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
                
                # Check for NaN values after conversion
                nan_count = result_df[col].isna().sum() - original_values.isna().sum()
                if nan_count > 0:
                    logger.warning(f"Conversion to numeric resulted in {nan_count} new NaN values in column '{col}'")
                else:
                    logger.debug(f"Successfully converted column '{col}' to numeric")
            except Exception as e:
                logger.error(f"Error converting column '{col}' to numeric: {str(e)}")
    
    return result_df

def handle_missing_values(df: pd.DataFrame, strategy: str = 'none', 
                         fill_values: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Handle missing values in DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        strategy (str): Strategy for handling missing values ('none', 'drop', 'fill')
        fill_values (Optional[Dict[str, Any]]): Dictionary mapping column names to fill values
    
    Returns:
        pd.DataFrame: DataFrame with missing values handled
    """
    if df is None or df.empty:
        return df
    
    result_df = df.copy()
    
    if strategy == 'drop':
        # Drop rows with any missing values
        original_row_count = len(result_df)
        result_df = result_df.dropna()
        dropped_rows = original_row_count - len(result_df)
        if dropped_rows > 0:
            logger.info(f"Dropped {dropped_rows} rows with missing values")
    
    elif strategy == 'fill' and fill_values:
        # Fill missing values with specified values
        result_df = result_df.fillna(fill_values)
        logger.debug(f"Filled missing values using provided values: {fill_values}")
    
    return result_df

def transform_dataframes(df1: pd.DataFrame, df2: Optional[pd.DataFrame] = None, 
                        column_mapping1: Optional[Dict[str, str]] = None,
                        column_mapping2: Optional[Dict[str, str]] = None,
                        time_column: str = 'timestamp',
                        time_format: Optional[str] = None,
                        numeric_columns: Optional[List[str]] = None,
                        missing_value_strategy: str = 'none',
                        fill_values: Optional[Dict[str, Any]] = None) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Transform one or two dataframes to standardize column names, time formats, and numeric columns.
    
    Args:
        df1 (pd.DataFrame): First DataFrame to transform
        df2 (Optional[pd.DataFrame]): Second DataFrame to transform (optional)
        column_mapping1 (Optional[Dict[str, str]]): Mapping for first DataFrame's columns
        column_mapping2 (Optional[Dict[str, str]]): Mapping for second DataFrame's columns
        time_column (str): Name of the column containing timestamps
        time_format (Optional[str]): Optional datetime format string for parsing
        numeric_columns (Optional[List[str]]): List of column names that should be numeric
        missing_value_strategy (str): Strategy for handling missing values ('none', 'drop', 'fill')
        fill_values (Optional[Dict[str, Any]]): Dictionary mapping column names to fill values
    
    Returns:
        Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]: Transformed DataFrame(s)
    """
    # Validate inputs
    if df1 is None:
        logger.error("First DataFrame (df1) is required but was None")
        raise ValueError("First DataFrame (df1) is required")
    
    # Default numeric columns if not specified
    if numeric_columns is None:
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
    
    # Transform the first DataFrame
    logger.info("Transforming first DataFrame")
    transformed_df1 = standardize_column_names(df1, column_mapping1)
    transformed_df1 = standardize_time_format(transformed_df1, time_column, time_format)
    transformed_df1 = ensure_numeric_columns(transformed_df1, numeric_columns)
    transformed_df1 = handle_missing_values(transformed_df1, missing_value_strategy, fill_values)
    
    # Transform the second DataFrame if provided
    if df2 is not None:
        logger.info("Transforming second DataFrame")
        transformed_df2 = standardize_column_names(df2, column_mapping2 or column_mapping1)
        transformed_df2 = standardize_time_format(transformed_df2, time_column, time_format)
        transformed_df2 = ensure_numeric_columns(transformed_df2, numeric_columns)
        transformed_df2 = handle_missing_values(transformed_df2, missing_value_strategy, fill_values)
        return transformed_df1, transformed_df2
    
    return transformed_df1