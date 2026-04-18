from datetime import time
from dataclasses import dataclass
from typing import Optional, List

from restaurant.enums import CuisineType, Category


@dataclass
class CreateRestaurantDTO:
    name: str
    owner_email: str
    description: str
    cuisine_type: CuisineType
    address: str
    pin_code: str
    is_veg_only: bool
    is_active: bool


@dataclass
class RestaurantDTO:
    restaurant_id: str
    name: str
    owner_email: str
    description: str
    cuisine_type: CuisineType
    address: str
    pin_code: str
    is_veg_only: bool
    is_active: bool


@dataclass
class CreateRestaurantTimingDTO:
    restaurant_id: str
    day_of_week: int
    open_time: time
    close_time: time


@dataclass
class UpdateRestaurantTimingDTO:
    id: int
    user_id: str
    open_time: Optional[time]
    close_time:Optional[time]


@dataclass
class RestaurantTimingDTO:
    id: int
    restaurant_id: str
    day_of_week: int
    open_time: time
    close_time: time


@dataclass
class CreateMenuItemDTO:
    name: str
    description: str
    restaurant_id: str
    category: Category
    price: float
    is_veg: bool
    is_available: bool
    preparation_time_in_minutes: int
    tags: List[str]


@dataclass
class MenuItemDTO:
    item_id: str
    restaurant_id: str
    name: str
    description: str
    price: float
    is_veg: bool
    is_available: bool
    preparation_time_in_minutes: int
    tags: List[str]
    category: Category





