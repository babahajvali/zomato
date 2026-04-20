from datetime import time
from dataclasses import dataclass
from typing import Optional, List

from restaurant.constants.enums import CuisineType, Category


@dataclass
class CreateRestaurantDTO:
    name: str
    owner_id: str
    description: str
    cuisine_type: CuisineType
    address: str
    pin_code: str
    is_veg_only: bool
    is_deleted: bool


@dataclass
class RestaurantDTO:
    id: str
    name: str
    owner_id: str
    description: str
    cuisine_type: CuisineType
    address: str
    pin_code: str
    is_veg_only: bool
    is_deleted: bool


@dataclass
class CreateRestaurantTimingDTO:
    restaurant_id: str
    day_of_week: int
    open_time: time
    close_time: time


@dataclass
class UpdateRestaurantTimingDTO:
    timing_id: int
    user_id: str
    open_time: Optional[time]
    close_time: Optional[time]


@dataclass
class DeleteRestaurantTimingDTO:
    timing_id: int
    user_id: str


@dataclass
class RestaurantTimingDTO:
    timing_id: int
    restaurant_id: str
    day_of_week: int
    open_time: time
    close_time: time


@dataclass
class CreateMenuItemDTO:
    name: str
    description: str
    category: Category
    price: float
    is_veg: bool
    is_available: bool
    preparation_time_in_minutes: int
    tags: List[str]


@dataclass
class MenuItemDTO:
    id: str
    restaurant_id: str
    name: str
    description: str
    price: float
    is_veg: bool
    is_available: bool
    preparation_time_in_minutes: int
    tags: List[str]
    category: Category


@dataclass
class BrowseRestaurantFiltersDTO:
    cuisine_type: Optional[CuisineType] = None
    is_veg_only: Optional[bool] = None
    pincode: Optional[str] = None
    min_rating: Optional[float] = None
    search: Optional[str] = None
    limit: int = 10
    offset: int = 0


@dataclass
class BrowseRestaurantDTO:
    restaurant_id: str
    name: str
    description: str
    cuisine_type: CuisineType
    address: str
    pin_code: str
    is_veg_only: bool
    is_deleted: bool
    average_rating: float
    total_reviews: int
    is_open: bool = False


@dataclass
class MenuItemWithTagsDTO:
    item_id: str
    name: str
    description: str
    price: float
    category: Category
    is_veg: bool
    is_available: bool
    preparation_time_in_minutes: int
    tags: List[str]


@dataclass
class CategoryMenuDTO:
    category: Category
    items: List[MenuItemWithTagsDTO]


@dataclass
class RestaurantMenuDTO:
    restaurant_id: str
    categories: List[CategoryMenuDTO]
