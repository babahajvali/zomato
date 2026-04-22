class AlreadyExistsPromoCode(Exception):
    def __init__(self, codes):
        self.codes = codes


class DuplicatePromoCodes(Exception):
    def __init__(self, codes):
        self.codes = codes


class EmptyPromoCodeFound(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidPromoCodeDateRange(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class PromoCodeNotFound(Exception):
    def __init__(self, promo_code_id: int):
        self.promo_code_id = promo_code_id

    def __str__(self):
        return f"PromoCode {self.promo_code_id} not found"


class PromoCodeMaximumUsed(Exception):
    def __init__(self, max_usage_count: int):
        self.max_usage_count = max_usage_count

    def __str__(self):
        return f"Maximum usage count {self.max_usage_count}"


class PromoCodeNotEligible(Exception):
    def __init__(self, min_order_value: float, items_total: float):
        self.min_order_value = min_order_value
        self.items_total = items_total

    def __str__(self):
        return f"Minimum order value {self.min_order_value} is greater than total items {self.items_total}"


class InvalidDeliveryZoneFound(Exception):
    def __init__(self, restaurant_id: str, pin_code: str):
        self.restaurant_id = restaurant_id
        self.pin_code = pin_code

    def __str__(self):
        return f"This {self.restaurant_id} not delivered at this zone {self.pin_code}"


class InvalidAddressFound(Exception):
    def __init__(self, address_id: int):
        self.address_id = address_id

    def __str__(self):
        return f"Invalid address {self.address_id}"


class RestaurantDayTimingNotFound(Exception):
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
