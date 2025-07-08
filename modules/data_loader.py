import pandas as pd
from datetime import datetime, time

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV data into a pandas DataFrame and perform minimal preprocessing.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded and preprocessed DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        
        # Convert 'Timestamp' column to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Ensure column names follow a consistent naming convention
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
        
        # Handle missing values (if any)
        df = df.fillna(method='ffill')  # Forward fill missing values
        
        # Ensure numeric columns are of the correct type
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    except Exception as e:
        raise ValueError(f"Error loading data: {str(e)}")

def isforbiddentime(df: pd.DataFrame, index: int) -> bool:
    """
    Check if the given timestamp is within forbidden trading hours.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data.
        index (int): Index of the row to check.
    
    Returns:
        bool: True if it's a forbidden time, False otherwise.
    """
    timestamp = df['timestamp'].iloc[index]
    current_time = timestamp.time()
    
    morning_start = time(9, 15)
    morning_end = time(9, 20)
    evening_start = time(15, 20)
    evening_end = time(15, 30)
    
    return (morning_start <= current_time <= morning_end) or (evening_start <= current_time <= evening_end)

def isOpencandle(df: pd.DataFrame, index: int) -> bool:
    """
    Check if the given candle is an opening candle.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data.
        index (int): Index of the row to check.
    
    Returns:
        bool: True if it's an opening candle, False otherwise.
    """
    timestamp = df['timestamp'].iloc[index]
    current_time = timestamp.time()
    
    opening_time = time(9, 15)
    
    return current_time == opening_time