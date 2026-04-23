from typing import List

from restaurants.interactors.dtos import (
    DeliveryZoneDTO,
    RestaurantTimingDTO,
    CartItemDTO,
)
from restaurants.storages.cart_storage import CartStorage
from restaurants.storages.delivery_zone_storage import DeliveryZoneStorage
from restaurants.storages.restaurant_storage import RestaurantStorage
from restaurants.storages.restaurant_timing_storage import RestaurantTimingStorage


class ServiceInterface:
    def __init__(self):
        self.cart_storage = CartStorage()
        self.delivery_zone_storage = DeliveryZoneStorage()
        self.restaurant_timing_storage = RestaurantTimingStorage()
        self.restaurant_storage = RestaurantStorage()

    def get_delivery_zone_by_restaurant_id(
        self, restaurant_id: str, pin_code: str
    ) -> DeliveryZoneDTO | None:

        zone_dto = self.delivery_zone_storage.get_restaurant_delivery_zones(
            restaurant_id=restaurant_id, pin_code=pin_code
        )

        return zone_dto

    def get_restaurant_timing(
        self, restaurant_id: str, day_of_week: int
    ) -> RestaurantTimingDTO | None:
        restaurant_day_timing = (
            self.restaurant_timing_storage.get_day_restaurant_timing(
                restaurant_id=restaurant_id, day_of_week=day_of_week
            )
        )

        return restaurant_day_timing

    def get_cart_items(self, cart_id: str) -> List[CartItemDTO]:
        return self.cart_storage.get_cart_items(cart_id=cart_id)

    def clear_cart_items(self, cart_id: str):

        return self.cart_storage.clear_cart_items(cart_id=cart_id)

    def get_customer_cart_id(self, customer_id: str) -> str:
        return self.cart_storage.get_customer_cart_id(customer_id=customer_id)

    def get_restaurant_owner_id(self, restaurant_id: str) -> str:
        return self.restaurant_storage.get_restaurant_owner_id(
            restaurant_id=restaurant_id
        )
