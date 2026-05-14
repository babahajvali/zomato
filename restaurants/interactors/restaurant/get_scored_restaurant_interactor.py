from decimal import Decimal, ROUND_HALF_UP
from typing import List

from restaurants.adapter.order import OrderAdapter
from restaurants.constants.constants import (
    DAY_FREQUENT,
    AVG_RATING,
    ORDER_VOLUME,
    TOTAL_REVIEWS,
    IS_OPEN,
)
from restaurants.interactors.dtos import ScoredRestaurantDTO, RestaurantDTO
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin


class GetScoredRestaurantInteractor(RestaurantMixin):
    def __init__(
        self,
        restaurant_storage: RestaurantStorageInterface,
        review_storage: ReviewStorageInterface,
    ):
        super().__init__(restaurant_storage=restaurant_storage)
        self.restaurant_storage = restaurant_storage
        self.review_storage = review_storage
        self.order_adapter = OrderAdapter()

    def get_scored_restaurant(
        self, pincode: str, limit: int, offset: int, user_id: str
    ) -> List[ScoredRestaurantDTO]:
        self.validate_limit_offset(limit=limit, offset=offset)
        restaurant_dtos = self.restaurant_storage.get_delivered_pincode_restaurants(
            pincode=pincode
        )

        restaurant_ids = [each.id for each in restaurant_dtos]

        reviews = self.review_storage.get_restaurants_reviews(
            restaurant_ids=restaurant_ids
        )
        reviews_map = {review.restaurant_id: review for review in reviews}

        order_stats = self.order_adapter.get_user_restaurants_stat(
            restaurant_ids=restaurant_ids, user_id=user_id
        )

        stats_map = {stat.restaurant_id: stat for stat in order_stats}
        scored = self._build_scored_dtos(
            restaurants=restaurant_dtos,
            stats_map=stats_map,
            reviews_map=reviews_map,
        )

        scored = self._calculate_scores(restaurants=scored)

        return scored[offset : offset + limit]

    def _build_scored_dtos(
        self, restaurants: List[RestaurantDTO], stats_map: dict, reviews_map: dict
    ) -> List[ScoredRestaurantDTO]:
        return [
            ScoredRestaurantDTO(
                restaurant_id=r.id,
                name=r.name,
                cuisine_type=r.cuisine_type,
                average_rating=Decimal(
                    reviews_map[r.id].avg_rating if r.id in reviews_map else 0.0
                ),
                total_reviews=(
                    reviews_map[r.id].total_reviews if r.id in reviews_map else 0
                ),
                is_open=True,
                order_volume=stats_map.get(r.id, self._empty_stats(r.id)).order_count,
                day_frequent=stats_map.get(
                    r.id, self._empty_stats(r.id)
                ).daily_frequent,
                score=Decimal(0.0),
            )
            for r in restaurants
        ]

    @staticmethod
    def _empty_stats(restaurant_id: str):
        from orders.app_service.dtos import RestaurantOrderStatsDTO

        return RestaurantOrderStatsDTO(
            restaurant_id=restaurant_id,
            order_count=0,
            daily_frequent=0,
        )

    @staticmethod
    def _calculate_scores(
        restaurants: List[ScoredRestaurantDTO],
    ) -> List[ScoredRestaurantDTO]:

        if not restaurants:
            return []

        max_frequency = max(r.day_frequent for r in restaurants) or 1
        max_volume = max(r.order_volume for r in restaurants) or 1
        max_reviews = max(r.total_reviews for r in restaurants) or 1

        for r in restaurants:
            norm_frequency = r.day_frequent / max_frequency
            norm_rating = float(r.average_rating) / 5.0
            norm_volume = r.order_volume / max_volume
            norm_reviews = r.total_reviews / max_reviews
            norm_is_open = 1.0

            r.score = Decimal(
                str(
                    round(
                        (norm_frequency * DAY_FREQUENT)
                        + (norm_rating * AVG_RATING)
                        + (norm_volume * ORDER_VOLUME)
                        + (norm_reviews * TOTAL_REVIEWS)
                        + (norm_is_open * IS_OPEN),
                        4,
                    )
                )
            ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        return sorted(
            restaurants,
            key=lambda r: r.score,
            reverse=True,
        )
