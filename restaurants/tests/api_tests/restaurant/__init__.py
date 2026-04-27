from utils.test_utils import GraphQLBaseTestCase


class BaseBrowseRestaurantsTestCase(GraphQLBaseTestCase):
    QUERY = """
    query BrowseRestaurants($params: BrowseRestaurantsInputParams!) {
      browseRestaurants(params: $params) {
        ... on BrowseRestaurantsType {
          __typename
          restaurants {
            restaurantId
            name
            description
            cuisineType
            address
            pinCode
            isVegOnly
            isDeleted
            isOpen
            averageRating
            totalReviews
          }
        }
        ... on InvalidCuisineTypeExceptionType {
          __typename
          cuisineType
        }
        ... on InvalidMinRatingExceptionType {
          __typename
          minRating
        }
      }
    }
    """


class BaseRestaurantMenuTestCase(GraphQLBaseTestCase):
    QUERY = """
    query RestaurantMenu($params: ViewRestaurantMenuInputParams!) {
    viewRestaurantManu(params: $params) {
    ... on RestaurantMenuType {
    __typename
    categories{
    category
    items{
    description
      isAvailable
      isVeg
      itemId
      name
      preparationTimeInMinutes
      price
      tags
    }
    }
    restaurantId
    }
    ... on RestaurantNotFoundType {
    __typename
    restaurantId
    }
    }
    }"""


class BaseCreateMenuItemsTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation CreateMenuItems($params: CreateMenuItemsInputParams!) {
      createMenuItems(params: $params) {
        ... on MenuItemsType {
          __typename
          menuItems {
            itemId
            restaurantId
            name
            description
            price
            category
            isVeg
            isAvailable
            preparationTimeInMinutes
            tags
          }
        }
        ... on RestaurantNotFoundType {
          __typename
          restaurantId
        }
        ... on InvalidCategoriesFoundType {
          __typename
          categories
        }
        ... on UserIsNotRestaurantOwnerType {
          __typename
          userId
        }
      }
    }
    """


class BaseGetRestaurantDashboardTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetRestaurantDashboard($params: GetRestaurantDashboardInputParams!) {
      getRestaurantDashboard(params: $params) {
        ... on RestaurantDashboardType {
          __typename
          ordersByStatus {
            count
            status
          }
          ratingSummary {
            averageRating
            totalReviews
            distribution
          }
          summary {
            avgOrderValue
            cancellationRate
            totalCancelled
            totalOrders
            totalRevenue
          }
        }
        ... on RestaurantNotFound {
          __typename
          restaurantId
        }
        ... on InvalidDateRange {
          __typename
          dateFrom
          dateTo
        }
        ... on UserIsNotRestaurantOwner {
          __typename
          userId
        }
      }
    }
    """
