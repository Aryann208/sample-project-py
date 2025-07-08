import unittest
import pytest
from modules.risk_management import calculate_stop_loss, RiskManager

class TestRiskManagement(unittest.TestCase):

    def setUp(self):
        self.risk_manager = RiskManager()

    @pytest.mark.parametrize("entry_price, trade_type, atr_value, expected", [
        (100, 'BUY', 2, 98),
        (100, 'SELL', 2, 102),
        (50, 'BUY', 1, 49),
        (50, 'SELL', 1, 51),
        (200, 'BUY', 5, 195),
        (200, 'SELL', 5, 205),
    ])
    def test_calculate_stop_loss(self, entry_price, trade_type, atr_value, expected):
        result = calculate_stop_loss(entry_price, trade_type, atr_value)
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_stop_loss_invalid_trade_type(self):
        with self.assertRaises(ValueError):
            calculate_stop_loss(100, 'INVALID', 2)

    def test_calculate_stop_loss_negative_price(self):
        with self.assertRaises(ValueError):
            calculate_stop_loss(-100, 'BUY', 2)

    def test_calculate_stop_loss_zero_atr(self):
        with self.assertRaises(ValueError):
            calculate_stop_loss(100, 'BUY', 0)

    def test_risk_manager_position_sizing(self):
        account_balance = 10000
        risk_per_trade = 0.02  # 2% risk
        entry_price = 100
        stop_loss = 95

        position_size = self.risk_manager.calculate_position_size(
            account_balance, risk_per_trade, entry_price, stop_loss
        )

        expected_position_size = (account_balance * risk_per_trade) / (entry_price - stop_loss)
        self.assertAlmostEqual(position_size, expected_position_size, places=2)

    def test_risk_manager_max_position_size(self):
        account_balance = 10000
        risk_per_trade = 0.02  # 2% risk
        entry_price = 100
        stop_loss = 99  # Very tight stop loss

        position_size = self.risk_manager.calculate_position_size(
            account_balance, risk_per_trade, entry_price, stop_loss
        )

        # Ensure position size doesn't exceed 20% of account balance
        max_position_size = account_balance * 0.2 / entry_price
        self.assertLessEqual(position_size, max_position_size)

    def test_risk_manager_assess_risk(self):
        current_price = 100
        entry_price = 95
        stop_loss = 90

        risk_assessment = self.risk_manager.assess_risk(current_price, entry_price, stop_loss)

        self.assertIn('risk_reward_ratio', risk_assessment)
        self.assertIn('risk_amount', risk_assessment)
        self.assertIn('potential_reward', risk_assessment)

        expected_risk_reward_ratio = (current_price - entry_price) / (entry_price - stop_loss)
        self.assertAlmostEqual(risk_assessment['risk_reward_ratio'], expected_risk_reward_ratio, places=2)

if __name__ == '__main__':
    unittest.main()