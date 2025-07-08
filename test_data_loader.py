import unittest
import pandas as pd
import numpy as np
from datetime import datetime, time
from io import StringIO
import pytest
from modules.data_loader import load_data, isforbiddentime, isOpencandle

class TestDataLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create sample data for testing
        cls.sample_csv = StringIO("""Timestamp,Open,High,Low,Close,Volume
2023-01-01 09:15:00,100,105,98,102,1000
2023-01-01 09:16:00,102,106,101,104,1200
2023-01-01 09:30:00,104,108,103,107,1500
2023-01-01 15:25:00,107,110,106,109,1800
""")
        cls.df = pd.read_csv(cls.sample_csv, parse_dates=['Timestamp'])

    def test_load_data(self):
        # Test load_data function
        df = load_data(StringIO(self.sample_csv.getvalue()))
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(list(df.columns), ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        self.assertEqual(len(df), 4)
        self.assertIsInstance(df['timestamp'].iloc[0], pd.Timestamp)
        self.assertTrue(all(df[col].dtype == np.float64 for col in ['open', 'high', 'low', 'close']))
        self.assertTrue(df['volume'].dtype == np.int64)

    def test_load_data_missing_values(self):
        # Test handling of missing values
        csv_with_missing = StringIO("""Timestamp,Open,High,Low,Close,Volume
2023-01-01 09:15:00,100,105,,102,1000
2023-01-01 09:16:00,102,106,101,,
""")
        df = load_data(csv_with_missing)
        self.assertFalse(df.isnull().any().any())  # No null values after forward fill

    @pytest.mark.parametrize("index, expected", [
        (0, True),   # 09:15:00
        (1, True),   # 09:16:00
        (2, False),  # 09:30:00
        (3, True),   # 15:25:00
    ])
    def test_isforbiddentime(self, index, expected):
        result = isforbiddentime(self.df, index)
        self.assertEqual(result, expected)

    @pytest.mark.parametrize("index, expected", [
        (0, True),   # 09:15:00
        (1, False),  # 09:16:00
        (2, False),  # 09:30:00
        (3, False),  # 15:25:00
    ])
    def test_isOpencandle(self, index, expected):
        result = isOpencandle(self.df, index)
        self.assertEqual(result, expected)

    def test_load_data_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            load_data("non_existent_file.csv")

    def test_load_data_performance(self):
        # Create a large DataFrame for performance testing
        large_df = pd.DataFrame({
            'Timestamp': pd.date_range(start='2023-01-01', periods=100000, freq='T'),
            'Open': np.random.rand(100000),
            'High': np.random.rand(100000),
            'Low': np.random.rand(100000),
            'Close': np.random.rand(100000),
            'Volume': np.random.randint(1000, 10000, 100000)
        })
        csv_file = StringIO(large_df.to_csv(index=False))
        
        import time
        start_time = time.time()
        _ = load_data(csv_file)
        end_time = time.time()
        
        self.assertLess(end_time - start_time, 5)  # Ensure loading takes less than 5 seconds

if __name__ == '__main__':
    unittest.main()