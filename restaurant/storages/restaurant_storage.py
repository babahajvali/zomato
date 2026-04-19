from typing import List

from account.models import User
from django.db.models import Avg, Count, Q

from restaurant.enums import Category
from restaurant.interactors.storage_interface.restaurant_storage_interface import \
    RestaurantStorageInterface
from restaurant.interactors.dtos import CreateRestaurantDTO, CreateMenuItemDTO, \
    MenuItemDTO, BrowseRestaurantDTO, BrowseRestaurantFiltersDTO, \
    MenuItemWithTagsDTO
from restaurant.exception.custom_exceptions import OwnerNotFound
from restaurant.models.restaurant import Restaurant, MenuItem


class RestaurantStorage(RestaurantStorageInterface):

    @staticmethod
    def _convert_to_menu_item_dto(item_obj: MenuItem) -> MenuItemDTO:
        return MenuItemDTO(
            item_id=item_obj.item_id,
            restaurant_id=item_obj.restaurant.restaurant_id,
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
            item_id=str(item.item_id),
            name=item.name,
            description=item.description,
            price=float(item.price),
            category=Category(item.category),
            is_veg=item.is_veg,
            is_available=item.is_available,
            preparation_time_in_minutes=item.preparation_time_in_minutes,
            tags=item.tags,
        )

    def create_bulk_restaurants(self,
                                restaurants_dto: List[CreateRestaurantDTO]):
        restaurants = []

        for dto in restaurants_dto:
            try:
                owner = User.objects.get(
                    email=dto.owner_email,
                    role='OWNER'
                )
            except User.DoesNotExist:
                raise OwnerNotFound(email=dto.owner_email)

            restaurant = Restaurant(
                name=dto.name,
                owner=owner,
                description=dto.description,
                cuisine_type=dto.cuisine_type,
                address=dto.address,
                pin_code=dto.pin_code,
                is_veg_only=dto.is_veg_only,
                is_active=dto.is_active
            )
            restaurants.append(restaurant)

        created_restaurants = Restaurant.objects.bulk_create(restaurants)

        return created_restaurants

    def get_existing_restaurants(self, names: List[str]) -> List[str]:
        return list(Restaurant.objects.filter(name__in=names)
                    .values_list('name', flat=True))

    def create_menu_items(
            self, create_items_dto: List[CreateMenuItemDTO]
    ) -> List[MenuItemDTO]:

        menu_items = [
            MenuItem(
                restaurant_id=item.restaurant_id,
                name=item.name,
                description=item.description,
                price=item.price,
                category=item.category.value,
                is_veg=item.is_veg,
                is_available=item.is_available,
                tags=item.tags,
                preparation_time_in_minutes=item.preparation_time_in_minutes,
            )
            for item in create_items_dto
        ]

        created_items = MenuItem.objects.bulk_create(menu_items)

        return [
            self._convert_to_menu_item_dto(item_obj=item)
            for item in created_items
        ]

    def get_restaurant_owner_id(self, restaurant_id: str) -> str:
        restaurant_data = Restaurant.objects.get(restaurant_id=restaurant_id)

        return restaurant_data.owner.user_id

    def check_restaurant_is_exist(self, restaurant_id: str) -> bool:
        return Restaurant.objects.filter(restaurant_id=restaurant_id).exists()

    def get_restaurants(self, filters_dto: BrowseRestaurantFiltersDTO) -> List[
        BrowseRestaurantDTO]:
        queryset = Restaurant.objects.filter(is_active=True).select_related(
            "owner")

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
            queryset = queryset.filter(
                Q(name__icontains=filters_dto.search)
                | Q(description__icontains=filters_dto.search)
            )

        queryset = queryset.annotate(
            average_rating=Avg("restaurantreview__rating"),
            total_reviews=Count("restaurantreview"),
        )

        if filters_dto.min_rating is not None:
            queryset = queryset.filter(
                average_rating__gte=filters_dto.min_rating)

        queryset = queryset.order_by("name")[
            filters_dto.offset: filters_dto.offset + filters_dto.limit
        ]

        return [
            BrowseRestaurantDTO(
                restaurant_id=str(restaurant.restaurant_id),
                name=restaurant.name,
                description=restaurant.description,
                cuisine_type=restaurant.cuisine_type,
                address=restaurant.address,
                pin_code=restaurant.pin_code,
                is_veg_only=restaurant.is_veg_only,
                is_active=restaurant.is_active,
                average_rating=float(restaurant.average_rating or 0.0),
                total_reviews=int(restaurant.total_reviews or 0),
            )
            for restaurant in queryset
        ]

    def get_available_menu_items_by_restaurant(
            self,
            restaurant_id: str,
    ) -> List[MenuItemWithTagsDTO]:

        items = (
            MenuItem.objects
            .filter(
                restaurant_id=restaurant_id,
                is_available=True,
            )
            .order_by('category', 'name')
        )

        return [
            self._convert_to_menu_item_with_tags_dto(item=item)
            for item in items
        ]

    def get_restaurants_by_ids(self, restaurant_ids: List[str]) -> List[str]:
        return list(Restaurant.objects.filter(restaurant_id__in=restaurant_ids).
                values_list('restaurant_id', flat=True))


