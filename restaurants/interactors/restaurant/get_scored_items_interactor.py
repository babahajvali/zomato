from decimal import Decimal, ROUND_HALF_UP
from typing import List

from restaurants.adapter.order import OrderAdapter
from restaurants.constants.constants import (
    RECENTLY_ORDERED,
    MOST_ORDERED,
    RESTAURANT_RATING,
    IS_AVAILABLE,
)
from restaurants.exception.custom_exceptions import (
    InvalidLimitFound,
    InvalidOffsetFound,
)
from restaurants.interactors.dtos import MenuItemScoredDTO, MenuItemWithTagsDTO
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin


class GetScoredItemsInteractor(RestaurantMixin):
    def __init__(
        self,
        restaurant_storage: RestaurantStorageInterface,
        review_storage: ReviewStorageInterface,
    ):
        super().__init__(restaurant_storage=restaurant_storage)
        self.restaurant_storage = restaurant_storage
        self.review_storage = review_storage
        self.order_adapter = OrderAdapter()

    def get_scored_restaurant_items(
        self,
        restaurant_id: str,
        user_id: str,
        limit: int,
        offset: int,
    ) -> List[MenuItemScoredDTO]:
        self._validate_limit_offset(limit=limit, offset=offset)
        self.validate_restaurant_exists(restaurant_id=restaurant_id)

        item_dtos = self.restaurant_storage.get_available_menu_items_by_restaurant(
            restaurant_id=restaurant_id
        )

        if not item_dtos:
            return []

        menu_item_ids = [each.item_id for each in item_dtos]

        rating_summary = self.review_storage.get_rating_summary(
            restaurant_id=restaurant_id
        )
        avg_rating = Decimal(str(rating_summary.average_rating or 0))

        menu_item_stats = self.order_adapter.get_menu_item_order_stats(
            menu_item_ids=menu_item_ids,
            user_id=user_id,
        )
        item_stats_map = {each.item_id: each for each in menu_item_stats}

        scored_items = self._build_menu_item_scored_dtos(
            item_dtos=item_dtos,
            average_rating=avg_rating,
            items_stat=item_stats_map,
            restaurant_id=restaurant_id,
        )

        scored_items = self._calculate_scores(items=scored_items)

        return scored_items[offset : offset + limit]

    @staticmethod
    def _validate_limit_offset(limit: int, offset: int):
        if limit < 0:
            raise InvalidLimitFound(limit=limit)

        if offset < 0:
            raise InvalidOffsetFound(offset=offset)

    def _build_menu_item_scored_dtos(
        self,
        item_dtos: List[MenuItemWithTagsDTO],
        average_rating: Decimal,
        items_stat: dict,
        restaurant_id: str,
    ) -> List[MenuItemScoredDTO]:

        return [
            MenuItemScoredDTO(
                restaurant_id=restaurant_id,
                menu_item_id=item.item_id,
                name=item.name,
                price=item.price,
                is_available=item.is_available,
                average_rating=average_rating,
                order_count=items_stat.get(
                    item.item_id, self._empty_stats(item.item_id)
                ).order_count,
                total_order_count=items_stat.get(
                    item.item_id, self._empty_stats(item.item_id)
                ).total_order_count,
                score=Decimal("0.0"),
            )
            for item in item_dtos
        ]

    @staticmethod
    def _calculate_scores(
        items: List[MenuItemScoredDTO],
    ) -> List[MenuItemScoredDTO]:

        if not items:
            return []

        max_recent = max((i.order_count for i in items), default=1) or 1
        max_total = max((i.total_order_count for i in items), default=1) or 1

        for item in items:
            norm_recent = item.order_count / max_recent
            norm_total = item.total_order_count / max_total
            norm_rating = float(item.average_rating) / 5.0
            norm_available = 1.0 if item.is_available else 0.0

            item.score = Decimal(
                str(
                    round(
                        (norm_recent * float(RECENTLY_ORDERED))
                        + (norm_total * float(MOST_ORDERED))
                        + (norm_rating * float(RESTAURANT_RATING))
                        + (norm_available * float(IS_AVAILABLE)),
                        4,
                    )
                )
            ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        return sorted(
            items,
            key=lambda i: i.score,
            reverse=True,
        )

    @staticmethod
    def _empty_stats(item_id: str):
        from restaurants.interactors.dtos import MenuItemOrderStatsDTO

        return MenuItemOrderStatsDTO(
            item_id=item_id,
            order_count=0,
            total_order_count=0,
        )
