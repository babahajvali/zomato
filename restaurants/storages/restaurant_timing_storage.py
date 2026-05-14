from typing import List

from restaurants.interactors.dtos import (
    CreateRestaurantTimingDTO,
    UpdateRestaurantTimingDTO,
    RestaurantTimingDTO,
    BulkUpdateRestaurantTimingDTO,
)
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.models.restaurant_timing import RestaurantTiming


class RestaurantTimingStorage(RestaurantTimingStorageInterface):
    @staticmethod
    def _convert_to_timing_dto(timing_obj: RestaurantTiming) -> RestaurantTimingDTO:
        return RestaurantTimingDTO(
            timing_id=timing_obj.pk,
            day_of_week=timing_obj.day_of_week,
            restaurant_id=timing_obj.restaurant_id,
            open_time=timing_obj.open_time,
            close_time=timing_obj.close_time,
        )

    def create_bulk_restaurant_timing(
        self, create_restaurant_timing_dto: List[CreateRestaurantTimingDTO]
    ) -> List[RestaurantTimingDTO]:
        timings = [
            RestaurantTiming(
                restaurant_id=each.restaurant_id,
                day_of_week=each.day_of_week,
                open_time=each.open_time,
                close_time=each.close_time,
            )
            for each in create_restaurant_timing_dto
        ]

        created_timings = RestaurantTiming.objects.bulk_create(timings)

        return [
            self._convert_to_timing_dto(timing_obj=data) for data in created_timings
        ]

    def update_bulk_restaurant_timings(
        self, update_restaurant_timing_dtos: List[BulkUpdateRestaurantTimingDTO]
    ) -> List[RestaurantTiming]:
        timings = [
            RestaurantTiming(
                id=dto.timing_id,
                open_time=dto.open_time,
                close_time=dto.close_time,
            )
            for dto in update_restaurant_timing_dtos
        ]

        RestaurantTiming.objects.bulk_update(timings, ["open_time", "close_time"])

        return timings

    def get_existing_restaurant_timings(
        self, combinations: List[tuple[str, int]]
    ) -> List[RestaurantTimingDTO]:
        if not combinations:
            return []

        timings = RestaurantTiming.objects.none()
        for restaurant_id, day_of_week in combinations:
            timings = timings | RestaurantTiming.objects.filter(
                restaurant_id=restaurant_id,
                day_of_week=day_of_week,
            )

        return [self._convert_to_timing_dto(timing_obj=data) for data in timings]

    def update_restaurant_timing(
        self, update_restaurant_timing_dto: UpdateRestaurantTimingDTO
    ):

        timing_properties = {}

        if update_restaurant_timing_dto.open_time is not None:
            timing_properties["open_time"] = update_restaurant_timing_dto.open_time

        if update_restaurant_timing_dto.close_time is not None:
            timing_properties["close_time"] = update_restaurant_timing_dto.close_time

        RestaurantTiming.objects.filter(
            pk=update_restaurant_timing_dto.timing_id
        ).update(**timing_properties)

        return self.get_restaurant_timing(
            timing_id=update_restaurant_timing_dto.timing_id
        )

    def get_restaurant_timing(self, timing_id: int) -> RestaurantTimingDTO | None:
        timing = RestaurantTiming.objects.filter(pk=timing_id).first()

        if timing is None:
            return None

        return self._convert_to_timing_dto(timing_obj=timing)

    def get_restaurant_owner_id(self, timing_id: int) -> str | None:
        owner_id = (
            RestaurantTiming.objects.filter(id=timing_id)
            .values_list("restaurant__owner_id", flat=True)
            .first()
        )

        return str(owner_id) if owner_id is not None else None

    def get_operating_hours_for_restaurants(
        self, restaurant_ids: List[str]
    ) -> List[RestaurantTimingDTO]:

        timings = RestaurantTiming.objects.filter(restaurant_id__in=restaurant_ids)

        return [self._convert_to_timing_dto(timing_obj=data) for data in timings]

    def delete_restaurant_timing(self, timing_id: int):
        return RestaurantTiming.objects.filter(pk=timing_id).delete()

    def get_restaurant_timings(self, restaurant_id: str) -> List[RestaurantTimingDTO]:
        timings = RestaurantTiming.objects.filter(restaurant_id=restaurant_id)
        return [self._convert_to_timing_dto(timing_obj=data) for data in timings]

    def get_day_restaurant_timing(
        self, restaurant_id: str, day_of_week: int
    ) -> RestaurantTimingDTO | None:
        restaurant_day_timing = RestaurantTiming.objects.filter(
            restaurant_id=restaurant_id, day_of_week=day_of_week
        ).first()

        if restaurant_day_timing is None:
            return None

        return self._convert_to_timing_dto(timing_obj=restaurant_day_timing)
