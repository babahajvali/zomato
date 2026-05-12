import uuid

import factory

from restaurants.constants.enums import Category, CuisineType
from restaurants.interactors.dtos import (
    BrowseRestaurantFiltersDTO,
    CategoryMenuDTO,
    CreateMenuItemDTO,
    CreateRestaurantTimingDTO,
    CreateRestaurantDTO,
    MenuItemDTO,
    MenuItemWithTagsDTO,
    RestaurantMenuDTO,
    RestaurantTimingDTO,
    RestaurantDTO,
    UpdateMenuItemDTO,
    CartDTO,
    CartItemDTO,
    DeliveryZoneDTO,
    CreateReviewDTO,
    ReviewDTO,
    RestaurantReviewSummaryDTO,
    RestaurantReviewDTO,
    RatingSummaryDTO,
)


class CreateRestaurantDTOFactory(factory.Factory):
    class Meta:
        model = CreateRestaurantDTO

    id = factory.Sequence(lambda n: f"restaurant-{n}")
    name = factory.Sequence(lambda n: f"Restaurant {n}")
    owner_id = factory.Sequence(lambda n: f"00000000-0000-0000-0000-{n:012d}")
    description = factory.Faker("sentence")
    cuisine_type = CuisineType.NORTH_INDIAN.value
    address = factory.Faker("address")
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    is_veg_only = False
    is_deleted = False


class CreateMenuItemDTOFactory(factory.Factory):
    class Meta:
        model = CreateMenuItemDTO

    id = factory.Sequence(lambda n: f"item-{n}")
    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    category = Category.STARTER
    price = 199.0
    is_veg = True
    is_available = True
    preparation_time_in_minutes = 15
    tags = factory.LazyFunction(list)


class MenuItemDTOFactory(factory.Factory):
    class Meta:
        model = MenuItemDTO

    id = factory.Sequence(lambda n: f"item-{n}")
    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    price = 199.0
    is_veg = True
    is_available = True
    preparation_time_in_minutes = 15
    tags = factory.LazyFunction(list)
    category = Category.STARTER


class UpdateMenuItemDTOFactory(factory.Factory):
    class Meta:
        model = UpdateMenuItemDTO

    menu_item_id = factory.Sequence(lambda n: f"item-{n}")
    name = factory.Sequence(lambda n: f"Updated Item {n}")
    is_available = True
    preparation_time_in_minutes = 20
    price = 299.0
    tags = factory.LazyFunction(list)


class CreateRestaurantTimingDTOFactory(factory.Factory):
    class Meta:
        model = CreateRestaurantTimingDTO

    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    day_of_week = 1
    open_time = "09:00:00"
    close_time = "21:00:00"


class MenuItemWithTagsDTOFactory(factory.Factory):
    class Meta:
        model = MenuItemWithTagsDTO

    item_id = factory.Sequence(lambda n: f"item-{n}")
    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    price = 199.0
    category = Category.STARTER
    is_veg = True
    is_available = True
    preparation_time_in_minutes = 15
    tags = factory.LazyFunction(list)


class CategoryMenuDTOFactory(factory.Factory):
    class Meta:
        model = CategoryMenuDTO

    category = Category.STARTER
    items = factory.LazyFunction(list)


class RestaurantMenuDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantMenuDTO

    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    categories = factory.LazyFunction(list)


class RestaurantTimingDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantTimingDTO

    timing_id = factory.Sequence(lambda n: n)
    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    day_of_week = 1
    open_time = "09:00:00"
    close_time = "21:00:00"


class RestaurantDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantDTO

    id = factory.Sequence(lambda n: f"restaurant-{n}")
    name = factory.Sequence(lambda n: f"Restaurant {n}")
    description = factory.Faker("sentence")
    owner_id = factory.Sequence(lambda n: f"00000000-0000-0000-0000-{n:012d}")
    cuisine_type = "NORTH_INDIAN"
    address = factory.Faker("address")
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    is_veg_only = False
    is_deleted = False


class CartDTOFactory(factory.Factory):
    class Meta:
        model = CartDTO

    cart_id = factory.Sequence(lambda n: f"cart-{n}")
    customer_id = factory.Sequence(lambda n: f"customer-{n}")


class CartItemDTOFactory(factory.Factory):
    class Meta:
        model = CartItemDTO

    cart_item_id = factory.Sequence(lambda n: n)
    cart_id = factory.Sequence(lambda n: f"cart-{n}")
    menu_item_id = factory.Sequence(lambda n: f"item-{n}")
    quantity = 2
    item_price = 350.0


class DeliveryZoneDTOFactory(factory.Factory):
    class Meta:
        model = DeliveryZoneDTO

    delivery_zone_id = factory.Sequence(lambda n: n + 1)
    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    delivery_fee = 30.0
    estimated_delivery_mins = 30


class CreateReviewDTOFactory(factory.Factory):
    class Meta:
        model = CreateReviewDTO

    restaurant_id = factory.LazyFunction(uuid.uuid4)
    customer_id = factory.LazyFunction(uuid.uuid4)
    rating = factory.Faker("random_int", min=1, max=5)
    review = factory.Faker("text", max_nb_chars=200)


class ReviewDTOFactory(factory.Factory):
    class Meta:
        model = ReviewDTO

    review_id = factory.Sequence(lambda n: n)
    restaurant_id = factory.LazyFunction(uuid.uuid4)
    customer_id = factory.LazyFunction(uuid.uuid4)
    rating = factory.Faker("random_int", min=1, max=5)
    review = factory.Faker("text", max_nb_chars=200)


class BrowseRestaurantFiltersDTOFactory(factory.Factory):
    class Meta:
        model = BrowseRestaurantFiltersDTO

    cuisine_type = None
    is_veg_only = None
    pincode = None
    min_rating = None


class RestaurantReviewSummaryDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantReviewSummaryDTO

    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    average_rating = 4.5
    total_reviews = 2


class RestaurantReviewDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantReviewDTO

    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    avg_rating = 4.5
    total_reviews = 2


class RatingSummaryDTOFactory(factory.Factory):
    class Meta:
        model = RatingSummaryDTO

    average_rating = 4.5
    total_reviews = 2
    distribution = factory.LazyFunction(
        lambda: {"1": 0, "2": 0, "3": 0, "4": 1, "5": 1}
    )
