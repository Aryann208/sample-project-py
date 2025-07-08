import unittest
import pytest
import pandas as pd
import numpy as np
from modules.trade_signal import generate_signal, TradingStrategy

class TestTradeSignal(unittest.TestCase):

    def setUp(self):
        self.trading_strategy = TradingStrategy()

    def create_mock_dataframe(self, stx, sar, adx, di_plus, di_minus, close):
        return pd.DataFrame({
            'stx': [stx],
            'sar': [sar],
            'adx': [adx],
            'di_plus': [di_plus],
            'di_minus': [di_minus],
            'close': [close]
        })

    @pytest.mark.parametrize("stx, sar, adx, di_plus, di_minus, close, expected_signal", [
        (70, 98, 30, 25, 20, 100, 'BUY'),   # Strong uptrend
        (30, 102, 30, 20, 25, 100, 'SELL'), # Strong downtrend
        (50, 100, 20, 22, 22, 100, 'NONE'), # No clear trend
        (80, 102, 35, 30, 15, 100, 'BUY'),  # Very strong buy signal
        (20, 98, 35, 15, 30, 100, 'SELL'),  # Very strong sell signal
        (60, 99, 15, 18, 18, 100, 'NONE'),  # Weak signals, no clear direction
    ])
    def test_generate_signal(self, stx, sar, adx, di_plus, di_minus, close, expected_signal):
        df = self.create_mock_dataframe(stx, sar, adx, di_plus, di_minus, close)
        signal = generate_signal(df, 0)
        self.assertEqual(signal, expected_signal)

    def test_generate_signal_empty_dataframe(self):
        df = pd.DataFrame()
        with self.assertRaises(KeyError):
            generate_signal(df, 0)

    def test_generate_signal_missing_indicators(self):
        df = pd.DataFrame({'close': [100]})
        with self.assertRaises(KeyError):
            generate_signal(df, 0)

    def test_generate_signal_index_out_of_range(self):
        df = self.create_mock_dataframe(50, 100, 25, 20, 20, 100)
        with self.assertRaises(IndexError):
            generate_signal(df, 1)

    def test_trading_strategy_stx(self):
        df = self.create_mock_dataframe(80, 100, 25, 20, 20, 100)
        self.assertTrue(self.trading_strategy.check_stx_buy(df, 0))
        self.assertFalse(self.trading_strategy.check_stx_sell(df, 0))

        df = self.create_mock_dataframe(20, 100, 25, 20, 20, 100)
        self.assertFalse(self.trading_strategy.check_stx_buy(df, 0))
        self.assertTrue(self.trading_strategy.check_stx_sell(df, 0))

    def test_trading_strategy_sar(self):
        df = self.create_mock_dataframe(50, 98, 25, 20, 20, 100)
        self.assertTrue(self.trading_strategy.check_sar_buy(df, 0))
        self.assertFalse(self.trading_strategy.check_sar_sell(df, 0))

        df = self.create_mock_dataframe(50, 102, 25, 20, 20, 100)
        self.assertFalse(self.trading_strategy.check_sar_buy(df, 0))
        self.assertTrue(self.trading_strategy.check_sar_sell(df, 0))

    def test_trading_strategy_adx(self):
        df = self.create_mock_dataframe(50, 100, 30, 25, 20, 100)
        self.assertTrue(self.trading_strategy.check_adx_buy(df, 0))
        self.assertFalse(self.trading_strategy.check_adx_sell(df, 0))

        df = self.create_mock_dataframe(50, 100, 30, 20, 25, 100)
        self.assertFalse(self.trading_strategy.check_adx_buy(df, 0))
        self.assertTrue(self.trading_strategy.check_adx_sell(df, 0))

if __name__ == '__main__':
    unittest.main()