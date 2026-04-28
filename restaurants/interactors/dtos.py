from datetime import time, date
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List, Dict

from restaurants.constants.enums import CuisineType, Category


@dataclass
class CreateRestaurantDTO:
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
    id: str
    restaurant_id: str
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


@dataclass
class CartDTO:
    cart_id: str
    customer_id: str


@dataclass
class CartItemDTO:
    cart_item_id: int
    cart_id: str
    menu_item_id: str
    quantity: int
    item_price: float


@dataclass
class CreateDeliveryZoneDTO:
    restaurant_id: str
    pin_code: str
    delivery_fee: float
    estimated_delivery_mins: int


@dataclass
class DeliveryZoneDTO:
    delivery_zone_id: int
    restaurant_id: str
    pin_code: str
    delivery_fee: float
    estimated_delivery_mins: int


@dataclass
class CreateReviewDTO:
    restaurant_id: str
    customer_id: str
    rating: int
    review: str


@dataclass
class ReviewDTO:
    review_id: int
    restaurant_id: str
    customer_id: str
    rating: int
    review: str


@dataclass
class RestaurantReviewSummaryDTO:
    restaurant_id: str
    average_rating: float
    total_reviews: int


@dataclass
class DashboardFiltersDTO:
    restaurant_id: str
    owner_id: str
    date_from: date
    date_to: date


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
class RatingSummaryDTO:
    average_rating: Decimal
    total_reviews: int
    distribution: Dict[str, int]


@dataclass
class RestaurantDashboardDTO:
    summary: RestaurantOrdersSummaryDTO
    orders_by_status: List[OrdersByStatusDTO]
    rating_summary: RatingSummaryDTO


@dataclass
class UpdateMenuItemDTO:
    menu_item_id: str
    name: Optional[str]
    is_available: Optional[bool]
    preparation_time_in_minutes: Optional[int]
    price: Optional[Decimal]
    tags: Optional[List[str]]
