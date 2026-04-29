from decimal import Decimal

from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import InvalidDateRange, RestaurantNotFound
from restaurants.graphql.types.types import (
    RestaurantDashboardType,
    RestaurantOrdersSummaryType,
    OrdersByStatusType,
    RatingSummaryType,
    TopSellingItemType,
    PeakHourType,
)
from restaurants.interactors.dtos import DashboardFiltersDTO, RestaurantDashboardDTO
from restaurants.interactors.restaurant.restaurant_dashboard_interactor import (
    RestaurantDashboardInteractor,
)
from restaurants.storages.restaurant_storage import RestaurantStorage
from restaurants.storages.review_storage import ReviewStorage
from utils.graphql_types import UserNotRestaurantOwner


def get_restaurant_dashboard_resolver(root, info, params):

    restaurant_storage = RestaurantStorage()
    review_storage = ReviewStorage()

    interactor = RestaurantDashboardInteractor(
        restaurant_storage=restaurant_storage,
        review_storage=review_storage,
    )

    dashboard_input = DashboardFiltersDTO(
        restaurant_id=params.restaurant_id,
        date_from=params.date_from,
        date_to=params.date_to,
        owner_id=info.context.user_id,
    )

    try:
        result = interactor.get_restaurant_dashboard(
            dashboard_filter_dto=dashboard_input
        )

        return _map_dashboard_dto_to_type(result=result)
    except custom_exceptions.InvalidDateRange as e:
        return InvalidDateRange(date_from=e.date_from, date_to=e.date_to)
    except custom_exceptions.RestaurantNotFound as e:
        return RestaurantNotFound(restaurant_id=e.restaurant_id)
    except custom_exceptions.UserNotRestaurantOwner as e:
        return UserNotRestaurantOwner(user_id=e.user_id)


def _map_dashboard_dto_to_type(result: RestaurantDashboardDTO):
    return RestaurantDashboardType(
        summary=RestaurantOrdersSummaryType(
            total_orders=result.summary.total_orders,
            total_revenue=result.summary.total_revenue,
            avg_order_value=result.summary.avg_order_value,
            total_cancelled=result.summary.total_cancelled,
            cancellation_rate=result.summary.cancellation_rate,
        ),
        peak_hours=[
            PeakHourType(hour=i.hour, order_count=i.order_count)
            for i in result.peak_hours
        ],
        top_selling=[
            TopSellingItemType(
                menu_item_id=i.menu_item_id,
                quantity=i.quantity_sold,
                revenue=Decimal(i.revenue),
            )
            for i in result.top_selling_items
        ],
        orders_by_status=[
            OrdersByStatusType(status=i.status, count=i.count)
            for i in result.orders_by_status
        ],
        rating_summary=RatingSummaryType(
            average_rating=result.rating_summary.average_rating,
            total_reviews=result.rating_summary.total_reviews,
            distribution=result.rating_summary.distribution,
        ),
    )
