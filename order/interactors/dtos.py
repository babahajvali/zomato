from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from order.constants.enums import OrderStatus


@dataclass
class CreatePromoCodeDTO:
    code: str
    discount_type: str
    discount_value: float
    min_order_value: float
    max_usage: int
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


@dataclass
class PromoCodeDTO:
    promo_code_id: int
    code: str
    discount_type: str
    discount_value: float
    min_order_value: float
    max_usage: int
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


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
    items_total: float
    delivery_fee: float
    tax_fee: float
    final_amount: float
    address_id: int


@dataclass
class OrderDTO:
    order_id: str
    customer_id: str
    restaurant_id: str
    promo_code_id: Optional[int]
    status: OrderStatus
    items_total: float
    delivery_fee: float
    tax_fee: float
    final_amount: float
    address_id: int


@dataclass
class CreateOrderItemDTO:
    order_id: str
    item_id: str
    quantity: int
    item_price: float
