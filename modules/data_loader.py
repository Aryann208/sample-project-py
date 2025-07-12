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
        print(file_path)
        df = pd.read_csv(file_path) 
        print(df)
        # Convert 'Timestamp' column to datetime (before renaming columns)
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        elif 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
         
        # Ensure column names follow a consistent naming convention 
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower() 
        
        # Convert timestamp column to datetime after renaming (if not done before)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
         
        # Handle missing values (using newer pandas syntax)
        df = df.fillna(method='ffill') if hasattr(df, 'fillna') else df.ffill()
         
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
    # Check if index is valid
    if index >= len(df) or index < 0:
        raise IndexError(f"Index {index} is out of bounds for DataFrame with {len(df)} rows")
    
    # Check if timestamp column exists
    if 'timestamp' not in df.columns:
        raise KeyError("Column 'timestamp' not found in DataFrame")
    
    timestamp = df['timestamp'].iloc[index] 
    
    # Ensure timestamp is a datetime object
    if not isinstance(timestamp, pd.Timestamp):
        timestamp = pd.to_datetime(timestamp)
    
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
    # Check if index is valid
    if index >= len(df) or index < 0:
        raise IndexError(f"Index {index} is out of bounds for DataFrame with {len(df)} rows")
    
    # Check if timestamp column exists
    if 'timestamp' not in df.columns:
        raise KeyError("Column 'timestamp' not found in DataFrame")
    
    timestamp = df['timestamp'].iloc[index] 
    
    # Ensure timestamp is a datetime object
    if not isinstance(timestamp, pd.Timestamp):
        timestamp = pd.to_datetime(timestamp)
    
    current_time = timestamp.time() 
     
    opening_time = time(9, 15) 
     
    return current_time == opening_time