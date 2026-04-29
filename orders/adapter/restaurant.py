from typing import List

from orders.adapter.dtos import DeliveryZoneDTO, RestaurantTimingDTO, CartItemDTO
from restaurants.interactors.dtos import MenuItemDTO


class RestaurantAdapter:
    @property
    def interface(self):

        from restaurants.app_service.service_interface import ServiceInterface

        return ServiceInterface()

    def get_delivery_zone_by_restaurant_id(
        self, restaurant_id: str, pin_code: str
    ) -> DeliveryZoneDTO:

        return self.interface.get_delivery_zone_by_restaurant_id(
            restaurant_id=restaurant_id, pin_code=pin_code
        )

    def get_restaurant_timing(
        self, restaurant_id: str, day_of_week: int
    ) -> RestaurantTimingDTO:
        restaurant_day_timing = self.interface.get_restaurant_timing(
            restaurant_id=restaurant_id, day_of_week=day_of_week
        )

        return restaurant_day_timing

    def get_customer_cart_id(self, customer_id: str) -> str:
        return self.interface.get_customer_cart_id(customer_id=customer_id)

    def clear_customer_cart_items(self, cart_id: str):
        return self.interface.clear_cart_items(cart_id=cart_id)

    def get_customer_cart_items(self, cart_id: str) -> List[CartItemDTO]:
        return self.interface.get_cart_items(cart_id=cart_id)

    def get_restaurant_owner_id(self, restaurant_id: str):
        return self.interface.get_restaurant_owner_id(restaurant_id=restaurant_id)

    def get_unavailable_menu_items(self, menu_item_ids: List[str]) -> List[str]:
        return self.interface.get_unavailable_menu_items(menu_item_ids=menu_item_ids)
