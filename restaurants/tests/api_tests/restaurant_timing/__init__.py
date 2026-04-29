from utils.test_utils import GraphQLBaseTestCase


class BaseCreateRestaurantTimingTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation CreateRestaurantTiming($params: CreateRestaurantTimingInputParams!) {
      createRestaurantTiming(params: $params) {
        ... on RestaurantTimingType {
          __typename
          id
          restaurantId
          dayOfWeek
          openTime
          closeTime
        }
        ... on RestaurantNotFound {
          __typename
          restaurantId
        }
        ... on UserNotRestaurantOwner {
          __typename
          userId
        }
        ... on InvalidTimingRange {
          __typename
          openTime
          closeTime
        }
      }
    }
    """


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
        ... on RestaurantTimingNotFound {
          __typename
          id
        }
        ... on UserNotRestaurantOwner {
          __typename
          userId
        }
        ... on InvalidTimingRange {
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
        ... on RestaurantNotFound {
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
        ... on RestaurantTimingNotFound {
          __typename
          id
        }
        ... on UserNotRestaurantOwner {
          __typename
          userId
        }
      }
    }
    """
