from order.adapter.dtos import DeliveryZoneDTO
from restaurant.app_service.service_interface import ServiceInterface


class RestaurantAdapter:
    @property
    def interface(self):

        return ServiceInterface()

    def get_delivery_zone_by_restaurant_id(
        self, restaurant_id: str, pin_code: str
    ) -> DeliveryZoneDTO | None:

        zones = self.interface.get_delivery_zone_by_restaurant_id(
            restaurant_id=restaurant_id, pin_code=pin_code
        )

        if zones is None:
            return None

        return zones
