from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List
from datetime import datetime

from orders.constants.enums import OrderStatus


@dataclass
class CreatePromoCodeDTO:
    id: int
    code: str
    discount_type: str
    discount_value: Decimal
    min_order_value: Decimal
    max_usage: int
    valid_from: datetime
    valid_until: datetime


@dataclass
class PromoCodeDTO:
    promo_code_id: int
    code: str
    discount_type: str
    discount_value: Decimal
    min_order_value: Decimal
    max_usage: int
    valid_from: datetime
    valid_until: datetime


@dataclass
class PlaceOrderDTO:
    customer_id: str
    restaurant_id: str
    promo_code_id: Optional[int]
    address_id: int


@dataclass
class CreateOrderDTO:
    customer_id: str
    restaurant_id: str
    promo_code_id: Optional[int]
    status: OrderStatus
    items_total: Decimal
    delivery_fee: Decimal
    tax_fee: Decimal
    final_amount: Decimal
    address_id: int


@dataclass
class OrderDTO:
    order_id: str
    customer_id: str
    restaurant_id: str
    promo_code_id: Optional[int]
    status: OrderStatus
    items_total: Decimal
    delivery_fee: Decimal
    tax_fee: Decimal
    final_amount: Decimal
    address_id: int
    placed_at: datetime


@dataclass
class CreateOrderItemDTO:
    order_id: str
    item_id: str
    quantity: int
    item_price: Decimal


@dataclass
class OrderItemSummaryDTO:
    item_id: str
    quantity: int
    item_price: Decimal
    subtotal: Decimal


@dataclass
class OrderSummaryDTO:
    order_id: str
    customer_id: str
    restaurant_id: str
    promo_code_id: Optional[int]
    status: OrderStatus
    items: List[OrderItemSummaryDTO]
    items_total: Decimal
    delivery_fee: Decimal
    tax_fee: Decimal
    final_amount: Decimal
    placed_at: datetime
    address_id: int


@dataclass
class TopSellingItemDTO:
    menu_item_id: str
    quantity_sold: int
    revenue: Decimal


@dataclass
class PeakHourDTO:
    hour: int
    order_count: int


@dataclass
class OrderItemDTO:
    order_id: str
    item_id: str
    quantity: int
    item_price: Decimal
    subtotal: Decimal
