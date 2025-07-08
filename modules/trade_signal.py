import pandas as pd
from abc import ABC, abstractmethod
from typing import List

class TradingStrategy(ABC):
    @abstractmethod
    def generate_signal(self, df: pd.DataFrame, index: int) -> str:
        pass

class STXStrategy(TradingStrategy):
    def generate_signal(self, df: pd.DataFrame, index: int) -> str:
        if df['stx'].iloc[index] > 80:
            return 'SELL'
        elif df['stx'].iloc[index] < 20:
            return 'BUY'
        return 'NONE'

class SARStrategy(TradingStrategy):
    def generate_signal(self, df: pd.DataFrame, index: int) -> str:
        if df['sar'].iloc[index] < df['close'].iloc[index]:
            return 'BUY'
        elif df['sar'].iloc[index] > df['close'].iloc[index]:
            return 'SELL'
        return 'NONE'

class ADXStrategy(TradingStrategy):
    def generate_signal(self, df: pd.DataFrame, index: int) -> str:
        if df['adx'].iloc[index] > 25:
            if df['di_plus'].iloc[index] > df['di_minus'].iloc[index]:
                return 'BUY'
            elif df['di_minus'].iloc[index] > df['di_plus'].iloc[index]:
                return 'SELL'
        return 'NONE'

class CompositeStrategy(TradingStrategy):
    def __init__(self, strategies: List[TradingStrategy]):
        self.strategies = strategies

    def generate_signal(self, df: pd.DataFrame, index: int) -> str:
        signals = [strategy.generate_signal(df, index) for strategy in self.strategies]
        if 'BUY' in signals and 'SELL' not in signals:
            return 'BUY'
        elif 'SELL' in signals and 'BUY' not in signals:
            return 'SELL'
        return 'NONE'

class SignalGenerator:
    def __init__(self, strategy: TradingStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: TradingStrategy):
        self.strategy = strategy

    def generate_signal(self, df: pd.DataFrame, index: int) -> str:
        return self.strategy.generate_signal(df, index)

def create_default_signal_generator() -> SignalGenerator:
    composite_strategy = CompositeStrategy([
        STXStrategy(),
        SARStrategy(),
        ADXStrategy()
    ])
    return SignalGenerator(composite_strategy)