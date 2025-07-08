import pandas as pd
import numpy as np
from typing import Dict, Any

class RiskStrategy:
    def calculate_stop_loss(self, entry_price: float, trade_type: str, **kwargs) -> float:
        raise NotImplementedError("Subclass must implement abstract method")

    def calculate_position_size(self, account_balance: float, risk_per_trade: float, **kwargs) -> float:
        raise NotImplementedError("Subclass must implement abstract method")

    def assess_risk(self, current_price: float, entry_price: float, stop_loss: float, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Subclass must implement abstract method")

class ATRBasedStopLoss(RiskStrategy):
    def calculate_stop_loss(self, entry_price: float, trade_type: str, atr_value: float, atr_multiplier: float = 2.0) -> float:
        if trade_type == 'BUY':
            return entry_price - (atr_value * atr_multiplier)
        elif trade_type == 'SELL':
            return entry_price + (atr_value * atr_multiplier)
        else:
            raise ValueError("Invalid trade type. Must be 'BUY' or 'SELL'.")

    def calculate_position_size(self, account_balance: float, risk_per_trade: float, entry_price: float, stop_loss: float) -> float:
        risk_amount = account_balance * (risk_per_trade / 100)
        position_size = risk_amount / abs(entry_price - stop_loss)
        return position_size

    def assess_risk(self, current_price: float, entry_price: float, stop_loss: float) -> Dict[str, Any]:
        risk = abs(entry_price - stop_loss)
        reward = abs(current_price - entry_price)
        risk_reward_ratio = reward / risk if risk != 0 else 0
        return {
            "risk": risk,
            "reward": reward,
            "risk_reward_ratio": risk_reward_ratio
        }

class FixedPercentageStopLoss(RiskStrategy):
    def calculate_stop_loss(self, entry_price: float, trade_type: str, percentage: float = 1.0) -> float:
        if trade_type == 'BUY':
            return entry_price * (1 - percentage / 100)
        elif trade_type == 'SELL':
            return entry_price * (1 + percentage / 100)
        else:
            raise ValueError("Invalid trade type. Must be 'BUY' or 'SELL'.")

    def calculate_position_size(self, account_balance: float, risk_per_trade: float, entry_price: float, stop_loss: float) -> float:
        risk_amount = account_balance * (risk_per_trade / 100)
        position_size = risk_amount / abs(entry_price - stop_loss)
        return position_size

    def assess_risk(self, current_price: float, entry_price: float, stop_loss: float) -> Dict[str, Any]:
        risk = abs(entry_price - stop_loss)
        reward = abs(current_price - entry_price)
        risk_reward_ratio = reward / risk if risk != 0 else 0
        return {
            "risk": risk,
            "reward": reward,
            "risk_reward_ratio": risk_reward_ratio
        }

class RiskManager:
    def __init__(self, strategy: RiskStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: RiskStrategy):
        self.strategy = strategy

    def calculate_stop_loss(self, entry_price: float, trade_type: str, **kwargs) -> float:
        return self.strategy.calculate_stop_loss(entry_price, trade_type, **kwargs)

    def calculate_position_size(self, account_balance: float, risk_per_trade: float, **kwargs) -> float:
        return self.strategy.calculate_position_size(account_balance, risk_per_trade, **kwargs)

    def assess_risk(self, current_price: float, entry_price: float, stop_loss: float, **kwargs) -> Dict[str, Any]:
        return self.strategy.assess_risk(current_price, entry_price, stop_loss, **kwargs)

def calculate_drawdown(equity_curve: pd.Series) -> float:
    """
    Calculate the maximum drawdown from a series of equity values.
    """
    cummax = equity_curve.cummax()
    drawdown = (cummax - equity_curve) / cummax
    return drawdown.max()

def track_risk_exposure(positions: Dict[str, Dict[str, Any]], account_balance: float) -> float:
    """
    Track overall risk exposure across multiple positions.
    """
    total_risk = sum(pos['risk_amount'] for pos in positions.values())
    return total_risk / account_balance

def adjust_risk_parameters(performance_metrics: Dict[str, float], current_parameters: Dict[str, float]) -> Dict[str, float]:
    """
    Dynamically adjust risk parameters based on recent performance.
    """
    # This is a placeholder implementation. In a real system, you'd use more sophisticated logic.
    if performance_metrics['win_rate'] > 0.6:
        current_parameters['risk_per_trade'] *= 1.1  # Increase risk slightly
    elif performance_metrics['win_rate'] < 0.4:
        current_parameters['risk_per_trade'] *= 0.9  # Decrease risk slightly
    
    return current_parameters