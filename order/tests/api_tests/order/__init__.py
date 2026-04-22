from utils.test_utils import GraphQLBaseTestCase


class BasePlaceOrderTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation PlaceOrder($params: PlaceOrderInputParams!) {
      placeOrder(params: $params) {
        ... on OrderType {
          __typename
          customerId
          restaurantId
          promoCodeId
          status
          itemsTotal
          deliveryFee
          taxFee
          finalAmount
          addressId
        }
        ... on PromoCodeNotFound {
          __typename
          promoCodeId
        }
        ... on PromoCodeMaximumUsed {
          __typename
          maxUsageCount
        }
        ... on PromoCodeNotEligible {
          __typename
          minOrderValue
          itemsTotal
        }
        ... on InvalidAddressFound {
          __typename
          addressId
        }
        ... on InvalidDeliveryZoneFound {
          __typename
          restaurantId
          pinCode
        }
        ... on RestaurantDayTimingNotFound {
          __typename
          restaurantId
          dayOfWeek
        }
        ... on RestaurantClosed {
          __typename
          restaurantId
        }
      }
    }
    """
