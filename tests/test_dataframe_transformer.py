import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from modules.dataframe_transformer import (
    standardize_column_names,
    standardize_time_format,
    ensure_numeric_columns,
    transform_dataframes
)


class TestDataFrameTransformer(unittest.TestCase):
    """Test cases for the DataFrame Transformer module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create sample DataFrames for testing
        self.df_original = pd.DataFrame({
            'Timestamp': ['2023-01-01 10:00:00', '2023-01-01 11:00:00', '2023-01-01 12:00:00'],
            'Open Price': [100.0, 101.0, 102.0],
            'High Price': [105.0, 106.0, 107.0],
            'Low Price': [99.0, 100.0, 101.0],
            'Close Price': [103.0, 104.0, 105.0],
            'Trading Volume': [1000, 1100, 1200],
            'Indicator A': [1.5, 2.5, 3.5],
            'Indicator B': ['1.5', '2.5', 'N/A']
        })
        
        # DataFrame with missing values
        self.df_with_missing = pd.DataFrame({
            'Timestamp': ['2023-01-01 10:00:00', '2023-01-01 11:00:00', '2023-01-01 12:00:00'],
            'Open': [100.0, np.nan, 102.0],
            'High': [105.0, 106.0, np.nan],
            'Low': [99.0, np.nan, 101.0],
            'Close': [103.0, 104.0, 105.0]
        })
        
        # DataFrame with invalid time format
        self.df_invalid_time = pd.DataFrame({
            'Timestamp': ['2023-01-01 10:00:00', 'invalid_date', '2023-01-01 12:00:00'],
            'Open': [100.0, 101.0, 102.0]
        })
        
        # Second DataFrame for testing transform_dataframes with two DataFrames
        self.df_second = pd.DataFrame({
            'Time': ['2023-01-01 10:00:00', '2023-01-01 11:00:00', '2023-01-01 12:00:00'],
            'Open Val': [200.0, 201.0, 202.0],
            'High Val': [205.0, 206.0, 207.0],
            'Low Val': [199.0, 200.0, 201.0],
            'Close Val': [203.0, 204.0, 205.0]
        })
        
        # Empty DataFrame for testing edge cases
        self.df_empty = pd.DataFrame()
    
    def test_standardize_column_names_default(self):
        """Test standardizing column names with default rules."""
        result = standardize_column_names(self.df_original)
        
        # Check that column names are lowercase and spaces are replaced with underscores
        self.assertIn('timestamp', result.columns)
        self.assertIn('open_price', result.columns)
        self.assertIn('high_price', result.columns)
        self.assertIn('trading_volume', result.columns)
        
        # Check that all column names are transformed
        for col in result.columns:
            self.assertEqual(col, col.lower())
            self.assertNotIn(' ', col)
    
    def test_standardize_column_names_mapping(self):
        """Test standardizing column names with custom mapping."""
        column_mapping = {
            'Open Price': 'open',
            'High Price': 'high',
            'Low Price': 'low',
            'Close Price': 'close',
            'Trading Volume': 'volume'
        }
        
        result = standardize_column_names(self.df_original, column_mapping)
        
        # Check that mapped columns are renamed correctly
        self.assertIn('open', result.columns)
        self.assertIn('high', result.columns)
        self.assertIn('low', result.columns)
        self.assertIn('close', result.columns)
        self.assertIn('volume', result.columns)
        
        # Check that unmapped columns remain unchanged
        self.assertIn('Timestamp', result.columns)
        self.assertIn('Indicator A', result.columns)
        self.assertIn('Indicator B', result.columns)
    
    def test_standardize_column_names_empty_df(self):
        """Test standardizing column names with an empty DataFrame."""
        result = standardize_column_names(self.df_empty)
        self.assertTrue(result.empty)
    
    def test_standardize_time_format(self):
        """Test standardizing time format."""
        result = standardize_time_format(self.df_original, 'Timestamp')
        
        # Check that Timestamp column is converted to datetime
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result['Timestamp']))
        
        # Check specific datetime values
        self.assertEqual(result['Timestamp'][0].year, 2023)
        self.assertEqual(result['Timestamp'][0].month, 1)
        self.assertEqual(result['Timestamp'][0].day, 1)
        self.assertEqual(result['Timestamp'][0].hour, 10)
    
    def test_standardize_time_format_already_datetime(self):
        """Test standardizing time format when column is already datetime."""
        df = pd.DataFrame({
            'Timestamp': pd.to_datetime(['2023-01-01 10:00:00', '2023-01-01 11:00:00'])
        })
        
        result = standardize_time_format(df, 'Timestamp')
        
        # Check that Timestamp column is still datetime
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result['Timestamp']))
        
        # Check that values are unchanged
        self.assertEqual(result['Timestamp'][0], pd.Timestamp('2023-01-01 10:00:00'))
    
    def test_standardize_time_format_invalid_data(self):
        """Test standardizing time format with invalid data."""
        # This should raise a ValueError because the time column doesn't exist
        with self.assertRaises(ValueError):
            standardize_time_format(self.df_original, 'NonExistentColumn')
    
    def test_ensure_numeric_columns(self):
        """Test ensuring columns are numeric."""
        numeric_columns = ['Indicator A', 'Indicator B']
        result = ensure_numeric_columns(self.df_original, numeric_columns)
        
        # Check that specified columns are numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(result['Indicator A']))
        self.assertTrue(pd.api.types.is_numeric_dtype(result['Indicator B']))
        
        # Check that 'N/A' is converted to NaN
        self.assertTrue(pd.isna(result['Indicator B'][2]))
        
        # Check that valid numeric strings are converted correctly
        self.assertEqual(result['Indicator B'][0], 1.5)
        self.assertEqual(result['Indicator B'][1], 2.5)
    
    def test_ensure_numeric_columns_missing_column(self):
        """Test ensuring numeric columns when a column is missing."""
        numeric_columns = ['Indicator A', 'NonExistentColumn']
        result = ensure_numeric_columns(self.df_original, numeric_columns)
        
        # Check that existing column is converted
        self.assertTrue(pd.api.types.is_numeric_dtype(result['Indicator A']))
        
        # Check that no error is raised for missing column
        self.assertNotIn('NonExistentColumn', result.columns)
    
    def test_transform_dataframes_single(self):
        """Test transforming a single DataFrame."""
        column_mapping = {
            'Open Price': 'open',
            'High Price': 'high',
            'Low Price': 'low',
            'Close Price': 'close',
            'Trading Volume': 'volume',
            'Timestamp': 'timestamp'
        }
        
        result_df1, result_df2 = transform_dataframes(
            self.df_original,
            column_mapping=column_mapping,
            time_column='timestamp',
            numeric_columns=['open', 'high', 'low', 'close', 'volume']
        )
        
        # Check that column names are standardized
        self.assertIn('timestamp', result_df1.columns)
        self.assertIn('open', result_df1.columns)
        self.assertIn('high', result_df1.columns)
        self.assertIn('low', result_df1.columns)
        self.assertIn('close', result_df1.columns)
        self.assertIn('volume', result_df1.columns)
        
        # Check that Timestamp is converted to datetime
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result_df1['timestamp']))
        
        # Check that numeric columns are numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(result_df1['open']))
        self.assertTrue(pd.api.types.is_numeric_dtype(result_df1['high']))
        self.assertTrue(pd.api.types.is_numeric_dtype(result_df1['low']))
        self.assertTrue(pd.api.types.is_numeric_dtype(result_df1['close']))
        self.assertTrue(pd.api.types.is_numeric_dtype(result_df1['volume']))
        
        # Check that second DataFrame is None
        self.assertIsNone(result_df2)
    
    def test_transform_dataframes_pair(self):
        """Test transforming a pair of DataFrames."""
        column_mapping1 = {
            'Open Price': 'open',
            'High Price': 'high',
            'Low Price': 'low',
            'Close Price': 'close',
            'Trading Volume': 'volume',
            'Timestamp': 'timestamp'
        }
        
        column_mapping2 = {
            'Time': 'timestamp',
            'Open Val': 'open',
            'High Val': 'high',
            'Low Val': 'low',
            'Close Val': 'close'
        }
        
        df1_result, df2_result = transform_dataframes(
            self.df_original,
            self.df_second,
            column_mapping=column_mapping1,
            time_column='timestamp',
            numeric_columns=['open', 'high', 'low', 'close', 'volume']
        )
        
        # Check first DataFrame
        self.assertIn('timestamp', df1_result.columns)
        self.assertIn('open', df1_result.columns)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df1_result['timestamp']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df1_result['open']))
        
        # Check second DataFrame - should use the same mapping as first DataFrame
        self.assertNotIn('timestamp', df2_result.columns)  # 'Time' wasn't mapped
        self.assertNotIn('open', df2_result.columns)       # 'Open Val' wasn't mapped
        
        # Test with separate mappings
        df1_result, df2_result = transform_dataframes(
            self.df_original,
            self.df_second,
            column_mapping=column_mapping1,  # First mapping
            time_column='timestamp',
            numeric_columns=['open', 'high', 'low', 'close', 'volume']
        )
        
        # Apply second mapping manually for comparison
        df2_mapped = standardize_column_names(self.df_second, column_mapping2)
        
        # Check that columns in second DataFrame are as expected
        self.assertNotEqual(set(df2_result.columns), set(df2_mapped.columns))
    
    def test_transform_dataframes_empty(self):
        """Test transforming an empty DataFrame."""
        result_df1, result_df2 = transform_dataframes(
            self.df_empty,
            numeric_columns=['open', 'high', 'low', 'close', 'volume']
        )
        
        # Check that result is still empty
        self.assertTrue(result_df1.empty)
        self.assertIsNone(result_df2)
    
    def test_transform_dataframes_missing_time_column(self):
        """Test transforming a DataFrame with missing time column."""
        df_no_time = pd.DataFrame({
            'Open': [100.0, 101.0],
            'Close': [103.0, 104.0]
        })
        
        # This should raise a ValueError because the time column doesn't exist
        with self.assertRaises(ValueError):
            transform_dataframes(df_no_time, time_column='Timestamp')
    
    def test_transform_dataframes_custom_numeric(self):
        """Test transforming with custom numeric columns."""
        custom_numeric = ['Open Price', 'Close Price']
        
        result_df1, _ = transform_dataframes(
            self.df_original,
            numeric_columns=custom_numeric
        )
        
        # Check that specified columns are numeric (after standardization)
        self.assertTrue(pd.api.types.is_numeric_dtype(result_df1['open_price']))
        self.assertTrue(pd.api.types.is_numeric_dtype(result_df1['close_price']))


if __name__ == '__main__':
    unittest.main()