from typing import List

from restaurant.interactors.dtos import CreateRestaurantTimingDTO, \
    UpdateRestaurantTimingDTO, RestaurantTimingDTO
from restaurant.interactors.storage_interface.restaurant_timing_storage_interface import \
    RestaurantTimingStorageInterface
from restaurant.models.restaurant_timing import RestaurantTiming


class RestaurantTimingStorage(RestaurantTimingStorageInterface):

    @staticmethod
    def convert_to_timing_dto(
            timing_obj: RestaurantTiming) -> RestaurantTimingDTO:
        return RestaurantTimingDTO(
            id=timing_obj.pk,
            day_of_week=timing_obj.day_of_week,
            restaurant_id=timing_obj.restaurant_id,
            open_time=timing_obj.open_time,
            close_time=timing_obj.close_time,
        )

    def create_bulk_restaurant_timing(
            self, create_restaurant_timing_dto: List[
                CreateRestaurantTimingDTO]) -> List[RestaurantTimingDTO]:
        timings = [RestaurantTiming(
            restaurant_id=each.restaurant_id,
            day_of_week=each.day_of_week,
            open_time=each.open_time,
            close_time=each.close_time,
        ) for each in create_restaurant_timing_dto]

        created_timings = RestaurantTiming.objects.bulk_create(timings)

        return [self.convert_to_timing_dto(timing_obj=data) for data in
                created_timings]

    def update_restaurant_timing(
            self, update_restaurant_timing_dto: UpdateRestaurantTimingDTO):

        timing_properties = {}

        if update_restaurant_timing_dto.open_time is not None:
            timing_properties[
                'open_time'] = update_restaurant_timing_dto.open_time

        if update_restaurant_timing_dto.close_time is not None:
            timing_properties[
                'close_time'] = update_restaurant_timing_dto.close_time

        RestaurantTiming.objects.filter(
            pk=update_restaurant_timing_dto.id).update(
            **timing_properties
        )

        return self.get_restaurant_timing(id=update_restaurant_timing_dto.id)

    def get_restaurant_timing(self, id: int) -> RestaurantTimingDTO | None:
        timing = RestaurantTiming.objects.filter(pk=id).first()

        if timing is None:
            return None

        return self.convert_to_timing_dto(timing_obj=timing)

    def get_restaurant_owner_id(self, id: int) -> str | None:
        timing_data = RestaurantTiming.objects.filter(
            pk=id).first()

        if timing_data is None:
            return None

        return str(timing_data.restaurant.owner.user_id)

    def get_operating_hours_for_restaurants(
            self, restaurant_ids: List[str]) -> List[RestaurantTimingDTO]:

        timings = RestaurantTiming.objects.filter(
            restaurant_id__in=restaurant_ids)

        return [self.convert_to_timing_dto(timing_obj=data) for data in
                timings]
