from restaurant.interactors.dtos import DeliveryZoneDTO, RestaurantTimingDTO
from restaurant.storages.cart_storage import CartStorage
from restaurant.storages.delivery_zone_storage import DeliveryZoneStorage
from restaurant.storages.restaurant_timing_storage import RestaurantTimingStorage


class ServiceInterface:
    def __init__(self):
        self.cart_storage = CartStorage()
        self.delivery_zone_storage = DeliveryZoneStorage()
        self.restaurant_timing_storage = RestaurantTimingStorage()

    def get_delivery_zone_by_restaurant_id(
        self, restaurant_id: str, pin_code: str
    ) -> DeliveryZoneDTO | None:

        zone_dto = self.delivery_zone_storage.get_restaurant_delivery_zones(
            restaurant_id=restaurant_id, pin_code=pin_code
        )
        if zone_dto is None:
            return None

        return zone_dto

    def get_restaurant_timing(
        self, restaurant_id: str, day_of_week: int
    ) -> RestaurantTimingDTO:
        pass
