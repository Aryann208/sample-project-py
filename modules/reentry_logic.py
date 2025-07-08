import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime, timedelta

class ReEntryStrategy(ABC):
    @abstractmethod
    def check_reentry(self, df: pd.DataFrame, index: int, last_trade: Dict[str, Any]) -> bool:
        pass

class TimeBased(ReEntryStrategy):
    def __init__(self, cooldown_period: timedelta):
        self.cooldown_period = cooldown_period

    def check_reentry(self, df: pd.DataFrame, index: int, last_trade: Dict[str, Any]) -> bool:
        if last_trade['exit_time'] is None:
            return False
        time_since_last_trade = df['timestamp'].iloc[index] - last_trade['exit_time']
        return time_since_last_trade >= self.cooldown_period

class PriceBased(ReEntryStrategy):
    def __init__(self, price_change_threshold: float):
        self.price_change_threshold = price_change_threshold

    def check_reentry(self, df: pd.DataFrame, index: int, last_trade: Dict[str, Any]) -> bool:
        if last_trade['exit_price'] is None:
            return False
        price_change = abs(df['close'].iloc[index] - last_trade['exit_price']) / last_trade['exit_price']
        return price_change >= self.price_change_threshold

class IndicatorBased(ReEntryStrategy):
    def check_reentry(self, df: pd.DataFrame, index: int, last_trade: Dict[str, Any]) -> bool:
        # Example: Re-enter if ADX is strong and price is above SMA
        adx_strong = df['adx'].iloc[index] > 25
        price_above_sma = df['close'].iloc[index] > df['sma'].iloc[index]
        return adx_strong and price_above_sma

class CompositeReEntryStrategy(ReEntryStrategy):
    def __init__(self, strategies: list[ReEntryStrategy]):
        self.strategies = strategies

    def check_reentry(self, df: pd.DataFrame, index: int, last_trade: Dict[str, Any]) -> bool:
        return all(strategy.check_reentry(df, index, last_trade) for strategy in self.strategies)

class ReEntryLogic:
    def __init__(self, strategy: ReEntryStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: ReEntryStrategy):
        self.strategy = strategy

    def check_reentry(self, df: pd.DataFrame, index: int, last_trade: Dict[str, Any]) -> bool:
        return self.strategy.check_reentry(df, index, last_trade)

def create_default_reentry_logic() -> ReEntryLogic:
    composite_strategy = CompositeReEntryStrategy([
        TimeBased(timedelta(minutes=30)),
        PriceBased(0.01),
        IndicatorBased()
    ])
    return ReEntryLogic(composite_strategy)