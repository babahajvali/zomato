from datetime import datetime
from decimal import Decimal
from typing import List

from django.db.models import Avg, Count, Q

from restaurants.constants.enums import Category
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.dtos import (
    CreateRestaurantDTO,
    CreateMenuItemDTO,
    MenuItemDTO,
    BrowseRestaurantFiltersDTO,
    MenuItemWithTagsDTO,
    RestaurantDTO,
    UpdateMenuItemDTO,
)
from restaurants.models.restaurant import Restaurant, MenuItem


class RestaurantStorage(RestaurantStorageInterface):
    @staticmethod
    def _convert_to_restaurant_dto(restaurant_obj: Restaurant) -> RestaurantDTO:
        return RestaurantDTO(
            id=str(restaurant_obj.id),
            name=restaurant_obj.name,
            description=restaurant_obj.description,
            cuisine_type=restaurant_obj.cuisine_type,
            address=restaurant_obj.address,
            pin_code=restaurant_obj.pin_code,
            is_veg_only=restaurant_obj.is_veg_only,
            is_deleted=restaurant_obj.is_deleted,
            owner_id=restaurant_obj.owner_id,
        )

    @staticmethod
    def _convert_to_menu_item_dto(item_obj: MenuItem) -> MenuItemDTO:
        return MenuItemDTO(
            id=item_obj.id,
            restaurant_id=item_obj.restaurant_id,
            name=item_obj.name,
            description=item_obj.description,
            price=item_obj.price,
            category=item_obj.category,
            is_veg=item_obj.is_veg,
            is_available=item_obj.is_available,
            tags=item_obj.tags,
            preparation_time_in_minutes=item_obj.preparation_time_in_minutes,
        )

    @staticmethod
    def _convert_to_menu_item_with_tags_dto(
        item: MenuItem,
    ) -> MenuItemWithTagsDTO:
        return MenuItemWithTagsDTO(
            item_id=str(item.id),
            name=item.name,
            description=item.description,
            price=Decimal(item.price),
            category=Category(item.category),
            is_veg=item.is_veg,
            is_available=item.is_available,
            preparation_time_in_minutes=item.preparation_time_in_minutes,
            tags=item.tags,
        )

    def create_bulk_restaurants(self, restaurant_dtos: List[CreateRestaurantDTO]):
        restaurants = []

        for dto in restaurant_dtos:
            restaurant = Restaurant(
                id=dto.id,
                name=dto.name,
                owner_id=dto.owner_id,
                description=dto.description,
                cuisine_type=dto.cuisine_type,
                address=dto.address,
                pin_code=dto.pin_code,
                is_veg_only=dto.is_veg_only,
                is_deleted=dto.is_deleted,
            )
            restaurants.append(restaurant)

        created_restaurants = Restaurant.objects.bulk_create(restaurants)

        return created_restaurants

    def get_existing_restaurants(self, names: List[str]) -> List[str]:
        return list(
            Restaurant.objects.filter(name__in=names).values_list("name", flat=True)
        )

    def create_menu_items(
        self, create_item_dtos: List[CreateMenuItemDTO], restaurant_id: str
    ) -> List[MenuItemDTO]:

        menu_items = [
            MenuItem(
                id=item.id,
                restaurant_id=item.restaurant_id,
                name=item.name,
                description=item.description,
                price=item.price,
                category=item.category.value
                if hasattr(item.category, "value")
                else item.category,
                is_veg=item.is_veg,
                is_available=item.is_available,
                tags=item.tags,
                preparation_time_in_minutes=item.preparation_time_in_minutes,
            )
            for item in create_item_dtos
        ]

        created_items = MenuItem.objects.bulk_create(menu_items)

        return [self._convert_to_menu_item_dto(item_obj=item) for item in created_items]

    def get_restaurant_owner_id(self, restaurant_id: str) -> str:
        restaurant_data = Restaurant.objects.get(id=restaurant_id)

        return restaurant_data.owner_id

    def check_restaurant_is_exist(self, restaurant_id: str) -> bool:
        return Restaurant.objects.filter(id=restaurant_id).exists()

    def get_restaurants(
        self, filters_dto: BrowseRestaurantFiltersDTO
    ) -> List[RestaurantDTO]:
        queryset = Restaurant.objects.filter(is_deleted=False)

        if filters_dto.cuisine_type:
            cuisine_type = (
                filters_dto.cuisine_type.value
                if hasattr(filters_dto.cuisine_type, "value")
                else str(filters_dto.cuisine_type)
            )
            queryset = queryset.filter(cuisine_type=cuisine_type)

        if filters_dto.is_veg_only is not None:
            queryset = queryset.filter(is_veg_only=filters_dto.is_veg_only)

        if filters_dto.pincode:
            queryset = queryset.filter(pin_code=filters_dto.pincode)

        if filters_dto.search:
            queryset = queryset.filter(Q(name__icontains=filters_dto.search))

        queryset = queryset.annotate(
            average_rating=Avg("restaurant_reviews__rating"),
            total_reviews=Count("restaurant_reviews"),
        )

        if filters_dto.min_rating is not None:
            queryset = queryset.filter(average_rating__gte=filters_dto.min_rating)

        queryset = queryset.order_by("name")[
            filters_dto.offset : filters_dto.offset + filters_dto.limit
        ]

        return [
            self._convert_to_restaurant_dto(restaurant_obj=restaurant)
            for restaurant in queryset
        ]

    def get_available_menu_items_by_restaurant(
        self, restaurant_id: str
    ) -> List[MenuItemWithTagsDTO]:

        items = MenuItem.objects.filter(
            restaurant_id=restaurant_id,
        ).order_by("category", "name")

        return [self._convert_to_menu_item_with_tags_dto(item=item) for item in items]

    def get_restaurants_by_ids(self, restaurant_ids: List[str]) -> List[str]:
        return list(
            Restaurant.objects.filter(id__in=restaurant_ids).values_list(
                "id", flat=True
            )
        )

    def get_menu_item(self, menu_item_id: str) -> MenuItemDTO | None:
        menu_item_obj = MenuItem.objects.filter(id=menu_item_id).first()

        if menu_item_obj is None:
            return None

        return self._convert_to_menu_item_dto(item_obj=menu_item_obj)

    def update_menu_item(self, update_menu_item_dto: UpdateMenuItemDTO) -> MenuItemDTO:

        update_properties = {}
        if update_menu_item_dto.name is not None:
            update_properties["name"] = update_menu_item_dto.name

        if update_menu_item_dto.price is not None:
            update_properties["price"] = update_menu_item_dto.price

        if update_menu_item_dto.is_available is not None:
            update_properties["is_available"] = update_menu_item_dto.is_available

        if update_menu_item_dto.preparation_time_in_minutes is not None:
            update_properties["preparation_time_in_minutes"] = (
                update_menu_item_dto.preparation_time_in_minutes
            )

        if update_menu_item_dto.tags is not None:
            update_properties["tags"] = update_menu_item_dto.tags

        MenuItem.objects.filter(id=update_menu_item_dto.menu_item_id).update(
            **update_properties
        )

        return self.get_menu_item(menu_item_id=update_menu_item_dto.menu_item_id)

    def delete_menu_item(self, menu_item_id: str):
        return MenuItem.objects.filter(id=menu_item_id).delete()

    def get_unavailable_menu_items(self, menu_item_ids: List[str]) -> List[str]:

        return list(
            MenuItem.objects.filter(
                id__in=menu_item_ids,
                is_available=False,
            ).values_list("id", flat=True)
        )

    def get_owner_restaurants(self, owner_id: str) -> List[RestaurantDTO]:
        restaurant_objs = Restaurant.objects.filter(
            owner_id=owner_id, is_deleted=False
        ).order_by("-created_at")

        return [
            RestaurantDTO(
                id=restaurant.id,
                name=restaurant.name,
                description=restaurant.description,
                cuisine_type=restaurant.cuisine_type,
                address=restaurant.address,
                pin_code=restaurant.pin_code,
                is_veg_only=restaurant.is_veg_only,
                is_deleted=restaurant.is_deleted,
                owner_id=owner_id,
            )
            for restaurant in restaurant_objs
        ]

    def get_delivered_pincode_restaurants(self, pincode: str) -> List[RestaurantDTO]:
        now = datetime.now()
        current_time = now.time()
        today_day = now.isoweekday()

        query = Restaurant.objects.filter(
            is_deleted=False,
            deliveryzone__pin_code=pincode,
            restauranttiming__day_of_week=today_day,
            restauranttiming__open_time__lte=current_time,
            restauranttiming__close_time__gte=current_time,
        ).distinct()

        return [self._convert_to_restaurant_dto(restaurant_obj=item) for item in query]
