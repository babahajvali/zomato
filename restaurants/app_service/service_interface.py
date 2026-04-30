from typing import List

from restaurants.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurants.interactors.delivery_zone.delivery_zone_interactor import (
    DeliveryZoneInteractor,
)
from restaurants.interactors.dtos import (
    DeliveryZoneDTO,
    RestaurantTimingDTO,
    CartItemDTO,
)
from restaurants.interactors.restaurant.browse_restaurants import (
    BrowseRestaurantsInteractor,
)
from restaurants.interactors.restaurant.menu_item_interactor import MenuItemInteractor
from restaurants.interactors.restaurant_timing.restaurant_timing_interactor import (
    RestaurantTimingInteractor,
)
from restaurants.storages.cart_storage import CartStorage
from restaurants.storages.delivery_zone_storage import DeliveryZoneStorage
from restaurants.storages.restaurant_storage import RestaurantStorage
from restaurants.storages.restaurant_timing_storage import RestaurantTimingStorage
from restaurants.storages.review_storage import ReviewStorage


class ServiceInterface:
    def __init__(self):
        self.cart_storage = CartStorage()
        self.delivery_zone_storage = DeliveryZoneStorage()
        self.restaurant_timing_storage = RestaurantTimingStorage()
        self.restaurant_storage = RestaurantStorage()
        self.review_storage = ReviewStorage()

    def get_delivery_zone_by_restaurant_id(
        self, restaurant_id: str, pin_code: str
    ) -> DeliveryZoneDTO:

        interactor = DeliveryZoneInteractor(
            delivery_zone_storage=self.delivery_zone_storage
        )

        return interactor.get_delivery_zone_by_restaurant_and_pin_code(
            restaurant_id=restaurant_id, pin_code=pin_code
        )

    def get_restaurant_timing(
        self, restaurant_id: str, day_of_week: int
    ) -> RestaurantTimingDTO:
        interactor = RestaurantTimingInteractor(
            restaurant_storage=self.restaurant_storage,
            restaurant_timing_storage=self.restaurant_timing_storage,
        )

        restaurant_day_timing = interactor.get_day_restaurant_timing(
            restaurant_id=restaurant_id, day_of_week=day_of_week
        )

        return restaurant_day_timing

    def get_cart_items(self, cart_id: str) -> List[CartItemDTO]:
        interactor = CartItemInteractor(
            cart_storage=self.cart_storage,
            restaurant_storage=self.restaurant_storage,
        )

        return interactor.get_cart_items(cart_id=cart_id)

    def clear_cart_items(self, cart_id: str):
        interactor = CartItemInteractor(
            cart_storage=self.cart_storage,
            restaurant_storage=self.restaurant_storage,
        )

        return interactor.clear_cart_items(cart_id=cart_id)

    def get_customer_cart_id(self, customer_id: str) -> str:
        interactor = CartItemInteractor(
            cart_storage=self.cart_storage,
            restaurant_storage=self.restaurant_storage,
        )

        return interactor.get_customer_cart_id(customer_id=customer_id)

    def get_restaurant_owner_id(self, restaurant_id: str) -> str:

        interactor = BrowseRestaurantsInteractor(
            restaurant_storage=self.restaurant_storage,
            restaurant_timing_storage=self.restaurant_timing_storage,
            review_storage=self.review_storage,
        )

        return interactor.get_restaurant_owner_id(restaurant_id=restaurant_id)

    def get_unavailable_menu_items(self, menu_item_ids: List[str]) -> List[str]:
        interactor = MenuItemInteractor(restaurant_storage=self.restaurant_storage)

        return interactor.get_unavailable_items(menu_item_ids=menu_item_ids)
