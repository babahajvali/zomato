from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RestaurantOrdersSummaryDTO:
    total_orders: int
    total_revenue: Decimal
    avg_order_value: Decimal
    total_cancelled: int
    cancellation_rate: Decimal


@dataclass
class OrdersByStatusDTO:
    status: str
    count: int


@dataclass
class RestaurantOrderStatsDTO:
    restaurant_id: str
    order_count: int
    daily_frequent: int


@dataclass
class MenuItemOrderStatsDTO:
    item_id: str
    order_count: int
    total_order_count: int
