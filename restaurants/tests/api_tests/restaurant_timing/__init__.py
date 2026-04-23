from utils.test_utils import GraphQLBaseTestCase


class BaseUpdateRestaurantTiming(GraphQLBaseTestCase):
    QUERY = """
    mutation UpdateRestaurantTiming($params: UpdateRestaurantTimingInputParams!) {
      updateRestaurantTiming(params: $params) {
        ... on RestaurantTimingType {
          __typename
          id
          restaurantId
          dayOfWeek
          openTime
          closeTime
        }
        ... on RestaurantTimingNoFoundTpe {
          __typename
          id
        }
        ... on UserIsNotRestaurantOwnerType {
          __typename
          userId
        }
        ... on OpenTimeGreaterThanCloseTimeType {
          __typename
          openTime
          closeTime
        }
      }
    }
    """


class BaseGetRestaurantTimingsTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetRestaurantTimings($params: GetRestaurantTimingsInputParams!) {
      getRestaurantTimings(params: $params) {
        ... on RestaurantTimingsListType {
          __typename
          timings {
            id
            restaurantId
            dayOfWeek
            openTime
            closeTime
          }
        }
        ... on RestaurantNotFoundType {
          __typename
          restaurantId
        }
      }
    }
    """


class BaseDeleteRestaurantTimingTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation DeleteRestaurantTiming($params: DeleteRestaurantTimingInputParams!) {
      deleteRestaurantTiming(params: $params) {
        ... on DeleteRestaurantTimingSuccessType {
          __typename
          success
          timingId
        }
        ... on RestaurantTimingNotFoundType {
          __typename
          id
        }
        ... on UserIsNotRestaurantOwnerType {
          __typename
          userId
        }
      }
    }
    """