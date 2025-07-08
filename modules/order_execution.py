from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any
import pandas as pd
from datetime import datetime

class OrderType(Enum):
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'
    STOP = 'STOP'

class OrderSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

class OrderStatus(Enum):
    PENDING = 'PENDING'
    EXECUTED = 'EXECUTED'
    CANCELLED = 'CANCELLED'

class Order:
    def __init__(self, symbol: str, side: OrderSide, order_type: OrderType, quantity: int, price: float = None):
        self.symbol = symbol
        self.side = side
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.status = OrderStatus.PENDING
        self.order_id = None
        self.execution_time = None

class ExecutionStrategy(ABC):
    @abstractmethod
    def execute(self, order: Order, current_price: float) -> Dict[str, Any]:
        pass

class MarketOrderStrategy(ExecutionStrategy):
    def execute(self, order: Order, current_price: float) -> Dict[str, Any]:
        order.status = OrderStatus.EXECUTED
        order.execution_time = datetime.now()
        return {
            "status": "success",
            "order_id": f"{order.side.value}-{order.symbol}-{order.execution_time.timestamp()}",
            "execution_price": current_price
        }

class LimitOrderStrategy(ExecutionStrategy):
    def execute(self, order: Order, current_price: float) -> Dict[str, Any]:
        if (order.side == OrderSide.BUY and current_price <= order.price) or \
           (order.side == OrderSide.SELL and current_price >= order.price):
            order.status = OrderStatus.EXECUTED
            order.execution_time = datetime.now()
            return {
                "status": "success",
                "order_id": f"{order.side.value}-{order.symbol}-{order.execution_time.timestamp()}",
                "execution_price": order.price
            }
        return {"status": "pending"}

class StopOrderStrategy(ExecutionStrategy):
    def execute(self, order: Order, current_price: float) -> Dict[str, Any]:
        if (order.side == OrderSide.BUY and current_price >= order.price) or \
           (order.side == OrderSide.SELL and current_price <= order.price):
            order.status = OrderStatus.EXECUTED
            order.execution_time = datetime.now()
            return {
                "status": "success",
                "order_id": f"{order.side.value}-{order.symbol}-{order.execution_time.timestamp()}",
                "execution_price": current_price
            }
        return {"status": "pending"}

class OrderFactory:
    @staticmethod
    def create_order(symbol: str, side: OrderSide, order_type: OrderType, quantity: int, price: float = None) -> Order:
        return Order(symbol, side, order_type, quantity, price)

class OrderExecutor:
    def __init__(self):
        self.strategies = {
            OrderType.MARKET: MarketOrderStrategy(),
            OrderType.LIMIT: LimitOrderStrategy(),
            OrderType.STOP: StopOrderStrategy()
        }
        self.orders = []

    def place_order(self, symbol: str, side: OrderSide, order_type: OrderType, quantity: int, price: float = None) -> Dict[str, Any]:
        order = OrderFactory.create_order(symbol, side, order_type, quantity, price)
        self.orders.append(order)
        return {"status": "Order placed", "order_id": id(order)}

    def execute_orders(self, current_prices: Dict[str, float]) -> List[Dict[str, Any]]:
        results = []
        for order in self.orders:
            if order.status == OrderStatus.PENDING:
                strategy = self.strategies[order.order_type]
                result = strategy.execute(order, current_prices[order.symbol])
                if result["status"] == "success":
                    order.order_id = result["order_id"]
                results.append(result)
        return results

    def get_order_status(self, order_id: int) -> OrderStatus:
        for order in self.orders:
            if id(order) == order_id:
                return order.status
        return None

    def cancel_order(self, order_id: int) -> bool:
        for order in self.orders:
            if id(order) == order_id and order.status == OrderStatus.PENDING:
                order.status = OrderStatus.CANCELLED
                return True
        return False

    def get_open_positions(self) -> Dict[str, int]:
        positions = {}
        for order in self.orders:
            if order.status == OrderStatus.EXECUTED:
                if order.symbol not in positions:
                    positions[order.symbol] = 0
                if order.side == OrderSide.BUY:
                    positions[order.symbol] += order.quantity
                else:
                    positions[order.symbol] -= order.quantity
        return positions

def calculate_profit_loss(orders: List[Order], current_prices: Dict[str, float]) -> float:
    pnl = 0
    for order in orders:
        if order.status == OrderStatus.EXECUTED:
            if order.side == OrderSide.BUY:
                pnl -= order.quantity * order.price
                pnl += order.quantity * current_prices[order.symbol]
            else:
                pnl += order.quantity * order.price
                pnl -= order.quantity * current_prices[order.symbol]
    return pnl