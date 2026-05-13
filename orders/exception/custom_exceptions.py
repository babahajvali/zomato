from datetime import datetime
from decimal import Decimal
from typing import List


class PromoCodeAlreadyExists(Exception):
    def __init__(self, codes: List[str]):
        self.codes = codes


class DuplicatePromoCodes(Exception):
    def __init__(self, codes: List[str]):
        self.codes = codes


class EmptyPromoCode(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class InvalidPromoCodeDateRange(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class PromoCodeNotFound(Exception):
    def __init__(self, promo_code_id: int):
        self.promo_code_id = promo_code_id

    def __str__(self):
        return f"PromoCode {self.promo_code_id} not found"


class PromoCodeUsageLimitReached(Exception):
    def __init__(self, max_usage_count: int):
        self.max_usage_count = max_usage_count

    def __str__(self):
        return f"Maximum usage count {self.max_usage_count}"


class PromoCodeNotEligible(Exception):
    def __init__(self, min_order_value: Decimal, items_total: Decimal):
        self.min_order_value = min_order_value
        self.items_total = items_total

    def __str__(self):
        return f"Minimum order value {self.min_order_value} is greater than total items {self.items_total}"


class DeliveryUnavailableForAddress(Exception):
    def __init__(self, restaurant_id: str, pin_code: str):
        self.restaurant_id = restaurant_id
        self.pin_code = pin_code

    def __str__(self):
        return f"This {self.restaurant_id} not delivered at this zone {self.pin_code}"


class AddressNotFound(Exception):
    def __init__(self, address_id: int):
        self.address_id = address_id

    def __str__(self):
        return f"Invalid address {self.address_id}"


class RestaurantNotOpen(Exception):
    def __init__(self, restaurant_id: str, day_of_week: int):
        self.restaurant_id = restaurant_id
        self.day_of_week = day_of_week

    def __str__(self):
        return f"Restaurant {self.restaurant_id} timing not found at this day {self.day_of_week}"


class RestaurantClosed(Exception):
    def __init__(self, restaurant_id: str):
        self.restaurant_id = restaurant_id

    def __str__(self):
        return f"Restaurant {self.restaurant_id} closed"


class ResourceLocked(Exception):
    def __init__(self, lock_key: str):
        self.lock_key = lock_key
        self.message = (
            "This resource is currently being modified. Please try again in a moment."
        )

    def __str__(self):
        return self.message


class CartIsEmpty(Exception):
    def __init__(self, cart_id: str):
        self.cart_id = cart_id

    def __str__(self):
        return f"Empty cart items found for {self.cart_id}"


class OrderNotFound(Exception):
    def __init__(self, order_id: str):
        self.order_id = order_id

    def __str__(self):
        return f"Order {self.order_id} not found"


class UserNotRestaurantOwner(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __str__(self):
        # TODO: returning the bare user_id leaks identifier to logs/error responses. Either a clear message or no __str__.
        return str(self.user_id)


class InvalidOrderStatusTransition(Exception):
    def __init__(
        self,
        current_status: str,
        new_status: str,
        allowed: list,
    ):
        self.current_status = current_status
        self.new_status = new_status
        self.allowed = allowed

    def __str__(self):
        return str(self.new_status)


class OrderNotOwnedByUser(Exception):
    def __init__(self, user_id: str, order_id: str):
        self.user_id = user_id
        self.order_id = order_id

    def __str__(self):
        return f"Order {self.order_id} does not belong to user {self.user_id}"


class OrderCancellationWindowExpired(Exception):
    def __init__(self, order_id: str, minutes: int):
        self.order_id = order_id
        self.minutes = minutes

    def __str__(self):
        return f"Order {self.order_id} cancellation time {self.minutes} exceeded"


class OrderCancellationNotAllowed(Exception):
    def __init__(self, order_id: str):
        self.order_id = order_id

    def __str__(self):
        return f"Order {self.order_id} can't be cancelled"


class PromoCodeNotYetValid(Exception):
    def __init__(self, code: str):
        self.code = code

    def __str__(self):
        return f"PromoCode {self.code} not yet valid"


class PromoCodeExpired(Exception):
    def __init__(self, code: str):
        self.code = code

    def __str__(self):
        return f"PromoCode {self.code} expired"


class OrderAlreadyCancelled(Exception):
    def __init__(self, order_id: str):
        self.order_id = order_id

    def __str__(self):
        return f"Order {self.order_id} already cancelled"


class CustomerCartNotFound(Exception):
    def __init__(self, customer_id: str):
        self.customer_id = customer_id

    def __str__(self):
        return f"Customer {self.customer_id} not found"


class MenuItemsUnavailable(Exception):
    def __init__(self, unavailable_item_ids: List[str]):
        self.unavailable_item_ids = unavailable_item_ids

    def __str__(self):
        return f"Unavailable menu items {self.unavailable_item_ids}"


class ScheduledTimeTooSoon(Exception):
    def __init__(self, scheduled_for: datetime):
        self.scheduled_for = scheduled_for

    def __str__(self):
        return f"Schedule time {self.scheduled_for}"


class RestaurantNotOpenAtScheduledTime(Exception):
    def __init__(self, restaurant_id: str, scheduled_for: datetime):
        self.restaurant_id = restaurant_id
        self.scheduled_for = scheduled_for

    def __str__(self):
        return f"This restaurant {self.restaurant_id} timing not found at scheduled time {self.scheduled_for}"
