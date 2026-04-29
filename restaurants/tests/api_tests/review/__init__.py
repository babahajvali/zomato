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
        ... on RestaurantNotFound {
          __typename
          restaurantId
        }
        ... on InvalidRatingFound {
          __typename
          userRating
        }
        ... on RestaurantAlreadyReviewedByUser {
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
        ... on RestaurantNotFound {
          __typename
          restaurantId
        }
      }
    }
    """


class BaseGetUserRestaurantReviewTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetUserRestaurantReview($params: GetUserRestaurantReviewInputParams!) {
      getUserRestaurantReview(params: $params) {
        ... on ReviewType {
          __typename
          reviewId
          restaurantId
          customerId
          rating
          review
        }
      }
    }
    """
