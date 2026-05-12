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
        ... on InvalidCuisineTypeException {
          __typename
          cuisineType
        }
        ... on InvalidMinRating {
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
    ... on RestaurantNotFound {
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
        ... on RestaurantNotFound {
          __typename
          restaurantId
        }
        ... on InvalidCategories {
          __typename
          categories
        }
        ... on UserNotRestaurantOwner {
          __typename
          userId
        }
      }
    }
    """


class BaseUpdateMenuItemTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation UpdateMenuItem($params: UpdateMenuItemInputParams!) {
      updateMenuItem(params: $params) {
        ... on MenuItemType {
          __typename
          category
          description
          isAvailable
          isVeg
          name
          itemId
          preparationTimeInMinutes
          price
          restaurantId
          tags
        }
        ... on MenuItemNotFound {
          __typename
          menuItemId
        }
        ... on UserNotRestaurantOwner {
          __typename
          userId
        }
      }
    }
    """


class BaseDeleteMenuItemTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation DeleteMenuItem($params: DeleteMenuItemInputParams!) {
      deleteMenuItem(params: $params) {
        ... on DeleteMenuItemSuccessType {
          __typename
          menuItemId
          success
        }
        ... on MenuItemNotFound {
          __typename
          menuItemId
        }
        ... on UserNotRestaurantOwner {
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
        ... on UserNotRestaurantOwner {
          __typename
          userId
        }
      }
    }
    """


class BaseGetOwnerRestaurantsTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetOwnerRestaurants {
      getOwnerRestaurants {
        ... on OwnerRestaurantsType {
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
            createdAt
            updatedAt
          }
        }
      }
    }
    """


class BaseGetScoredRestaurantsTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetUserRecommendedRestaurants($params: GetScoredRestaurantsInputParams!) {
      getUserRecommendedRestaurants(params: $params) {
        ... on ScoredRestaurantsType {
          __typename
          restaurants {
            restaurantId
            name
            cuisineType
            averageRating
            totalReviews
            score
            isOpen
            dayFrequent
            orderVolume
          }
        }
        ... on InvalidLimit {
          __typename
          limit
        }
        ... on InvalidOffset {
          __typename
          offset
        }
      }
    }
    """


class BaseGetScoredRestaurantItemsTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetScoredRestaurantItems($params: GetScoredRestaurantItemsInputParams!) {
      getScoredRestaurantItems(params: $params) {
        ... on ScoredItemsType {
          __typename
          menuItems {
            menuItemId
            restaurantId
            name
            price
            isAvailable
            totalOrdersCount
            recentlyOrderCount
            score
            averageRating
          }
        }
        ... on RestaurantNotFound {
          __typename
          restaurantId
        }
      }
    }
    """
