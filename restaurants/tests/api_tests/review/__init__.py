from utils.test_utils import GraphQLBaseTestCase


class BaseCreateReviewTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation CreateReview($params: CreateReviewInputParams!) {
      createReview(params: $params) {
        ... on ReviewType {
          __typename
          reviewId
          restaurantId
          customerId
          rating
          review
        }
        ... on RestaurantNotFoundType {
          __typename
          restaurantId
        }
        ... on InvalidRatingType {
          __typename
          rating
        }
        ... on UserAlreadyReviewedRestaurantType {
          __typename
          userId
        }
      }
    }
    """


class BaseGetRestaurantReviewsTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetRestaurantReviews($params: GetRestaurantReviewsInputParams!) {
      restaurantReviews(params: $params) {
        ... on ReviewsType {
          __typename
          reviews {
            reviewId
            restaurantId
            customerId
            rating
            review
          }
        }
        ... on RestaurantNotFoundType {
          __typename
          restaurantId
        }
      }
    }
    """
