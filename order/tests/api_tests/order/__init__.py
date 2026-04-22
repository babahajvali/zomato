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


class BaseUpdateOrderStatusTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation UpdateOrderStatus($params: UpdateOrderStatusInputParams!) {
      updateOrderStatus(params: $params) {
        ... on OrderType {
          __typename
          orderId
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
        ... on OrderNotFound {
          __typename
          orderId
        }
        ... on UserIsNotRestaurantOwner {
          __typename
          userId
        }
        ... on InvalidOrderStatusTransition {
          __typename
          currentStatus
          newStatus
          allowed
        }
      }
    }
    """


class BaseGetOrderTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetOrder($params: GetOrderInputParams!) {
      getOrder(params: $params) {
        ... on OrderType {
          __typename
          orderId
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
        ... on OrderNotFound {
          __typename
          orderId
        }
      }
    }
    """


class BaseUserOrdersTestCase(GraphQLBaseTestCase):
    QUERY = """
    query UserOrders {
      userOrders {
        ... on OrdersType {
          __typename
          orders {
            orderId
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
        }
      }
    }
    """


class BaseRestaurantOrdersTestCase(GraphQLBaseTestCase):
    QUERY = """
    query RestaurantOrders($params: GetRestaurantOrdersInputParams!) {
      restaurantOrders(params: $params) {
        ... on OrdersType {
          __typename
          orders {
            orderId
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
        }
        ... on UserIsNotRestaurantOwner {
          __typename
          userId
        }
      }
    }
    """


class BaseCancelOrderTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation CancelOrder($params: CancelOrderInputParams!) {
      cancelOrder(params: $params) {
        ... on OrderType {
          __typename
          orderId
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
        ... on OrderNotFoundType {
          __typename
          orderId
        }
        ... on OrderNotBelongsToUserType {
          __typename
          orderId
        }
        ... on OrderCancellationTimeExceededType {
          __typename
          orderId
        }
        ... on OrderCannotBeCancelledType {
          __typename
          orderId
        }
      }
    }
    """


class BaseAutoCancelOrderTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation AutoCancelOrder($params: AutoCancelOrderInputParams!) {
      autoCancelOrder(params: $params) {
        ... on OrderType {
          __typename
          orderId
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
        ... on OrderNotFoundType {
          __typename
          orderId
        }
        ... on OrderCannotBeCancelledType {
          __typename
          orderId
        }
      }
    }
    """
