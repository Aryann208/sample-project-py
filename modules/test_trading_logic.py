import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta
from modules.trading_logic import TradingLogic

class TestTradingLogic(unittest.TestCase):

    def setUp(self):
        self.mock_df = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='5T'),
            'open': [100] * 100,
            'high': [105] * 100,
            'low': [95] * 100,
            'close': [102] * 100,
            'volume': [1000] * 100
        })
        self.mock_df.set_index('timestamp', inplace=True)
        
        self.trading_logic = TradingLogic('TEST')

    @patch('modules.trade_signal.create_default_signal_generator')
    @patch('modules.risk_management.create_default_risk_manager')
    @patch('modules.reentry_logic.create_default_reentry_logic')
    @patch('modules.order_execution.OrderExecutor')
    def test_masterframe_normal_flow(self, mock_order_executor, mock_reentry_logic, mock_risk_manager, mock_signal_generator):
        # Setup mock return values
        mock_signal_generator.return_value.generate_signal.return_value = 'BUY'
        mock_risk_manager.return_value.assess_risk.return_value = {'allow_trade': True, 'position_size': 100, 'stop_loss': 98}
        mock_order_executor.return_value.place_order.return_value = {'status': 'Order placed', 'order_id': '123'}
        mock_order_executor.return_value.execute_orders.return_value = [{'status': 'success', 'order_id': '123'}]

        # Run the masterframe function
        _, _, trades = self.trading_logic.masterframe(self.mock_df, None)

        # Assertions
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]['side'], 'BUY')
        mock_signal_generator.return_value.generate_signal.assert_called()
        mock_risk_manager.return_value.assess_risk.assert_called()
        mock_order_executor.return_value.place_order.assert_called()
        mock_order_executor.return_value.execute_orders.assert_called()

    @patch('modules.trade_signal.create_default_signal_generator')
    @patch('modules.risk_management.create_default_risk_manager')
    @patch('modules.reentry_logic.create_default_reentry_logic')
    @patch('modules.order_execution.OrderExecutor')
    def test_masterframe_no_signal(self, mock_order_executor, mock_reentry_logic, mock_risk_manager, mock_signal_generator):
        # Setup mock return values
        mock_signal_generator.return_value.generate_signal.return_value = 'NONE'

        # Run the masterframe function
        _, _, trades = self.trading_logic.masterframe(self.mock_df, None)

        # Assertions
        self.assertEqual(len(trades), 0)
        mock_signal_generator.return_value.generate_signal.assert_called()
        mock_risk_manager.return_value.assess_risk.assert_not_called()
        mock_order_executor.return_value.place_order.assert_not_called()

    @patch('modules.trade_signal.create_default_signal_generator')
    @patch('modules.risk_management.create_default_risk_manager')
    @patch('modules.reentry_logic.create_default_reentry_logic')
    @patch('modules.order_execution.OrderExecutor')
    def test_masterframe_risk_assessment_fail(self, mock_order_executor, mock_reentry_logic, mock_risk_manager, mock_signal_generator):
        # Setup mock return values
        mock_signal_generator.return_value.generate_signal.return_value = 'BUY'
        mock_risk_manager.return_value.assess_risk.return_value = {'allow_trade': False}

        # Run the masterframe function
        _, _, trades = self.trading_logic.masterframe(self.mock_df, None)

        # Assertions
        self.assertEqual(len(trades), 0)
        mock_signal_generator.return_value.generate_signal.assert_called()
        mock_risk_manager.return_value.assess_risk.assert_called()
        mock_order_executor.return_value.place_order.assert_not_called()

    @patch('modules.trade_signal.create_default_signal_generator')
    @patch('modules.risk_management.create_default_risk_manager')
    @patch('modules.reentry_logic.create_default_reentry_logic')
    @patch('modules.order_execution.OrderExecutor')
    def test_masterframe_exit_condition(self, mock_order_executor, mock_reentry_logic, mock_risk_manager, mock_signal_generator):
        # Setup initial trade
        self.trading_logic.current_position = {
            'entry_price': 100,
            'quantity': 100,
            'side': 'BUY',
            'entry_time': datetime.now() - timedelta(hours=1),
            'stop_loss': 95
        }

        # Setup mock return values for exit
        mock_signal_generator.return_value.generate_signal.return_value = 'SELL'
        mock_order_executor.return_value.place_order.return_value = {'status': 'Order placed', 'order_id': '456'}
        mock_order_executor.return_value.execute_orders.return_value = [{'status': 'success', 'order_id': '456'}]

        # Run the masterframe function
        _, _, trades = self.trading_logic.masterframe(self.mock_df, None)

        # Assertions
        self.assertEqual(len(trades), 1)
        self.assertIn('exit_price', trades[0])
        self.assertIn('exit_time', trades[0])
        mock_order_executor.return_value.place_order.assert_called_with(
            symbol='TEST',
            side='SELL',
            order_type='MARKET',
            quantity=100,
            price=102
        )

    def test_check_exit_conditions(self):
        # Test stop loss
        position = {'side': 'BUY', 'stop_loss': 98}
        self.assertTrue(self.trading_logic.check_exit_conditions(pd.Series({'close': 97}), 0, position))

        # Test opposing signal
        position = {'side': 'BUY', 'stop_loss': 95}
        with patch('modules.trade_signal.create_default_signal_generator') as mock_signal_generator:
            mock_signal_generator.return_value.generate_signal.return_value = 'SELL'
            self.assertTrue(self.trading_logic.check_exit_conditions(pd.Series({'close': 100}), 0, position))

    @patch('modules.trade_signal.create_default_signal_generator')
    @patch('modules.risk_management.create_default_risk_manager')
    @patch('modules.reentry_logic.create_default_reentry_logic')
    @patch('modules.order_execution.OrderExecutor')
    def test_masterframe_performance(self, mock_order_executor, mock_reentry_logic, mock_risk_manager, mock_signal_generator):
        # Setup mock return values
        mock_signal_generator.return_value.generate_signal.return_value = 'NONE'

        # Create a larger DataFrame for performance testing
        large_df = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=10000, freq='5T'),
            'open': [100] * 10000,
            'high': [105] * 10000,
            'low': [95] * 10000,
            'close': [102] * 10000,
            'volume': [1000] * 10000
        })
        large_df.set_index('timestamp', inplace=True)

        import time
        start_time = time.time()
        self.trading_logic.masterframe(large_df, None)
        end_time = time.time()

        execution_time = end_time - start_time
        self.assertLess(execution_time, 5)  # Ensure execution takes less than 5 seconds

if __name__ == '__main__':
    unittest.main()