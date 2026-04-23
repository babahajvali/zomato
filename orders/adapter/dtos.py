from dataclasses import dataclass
from datetime import time


@dataclass
class AddressDTO:
    address_id: int
    full_address: str
    city: str
    pincode: str
    label: str
    is_default: bool
    user_id: str


@dataclass
class DeliveryZoneDTO:
    delivery_zone_id: int
    restaurant_id: str
    pin_code: str
    delivery_fee: float
    estimated_delivery_mins: int


@dataclass
class RestaurantTimingDTO:
    timing_id: int
    restaurant_id: str
    day_of_week: int
    open_time: time
    close_time: time


@dataclass
class CartItemDTO:
    cart_item_id: int
    cart_id: str
    menu_item_id: str
    quantity: int
    item_price: float
