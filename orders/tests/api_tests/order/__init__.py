from utils.test_utils import GraphQLBaseTestCase


class BasePlaceOrderTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation PlaceOrder($params: PlaceOrderInputParams!) {
      placeOrder(params: $params) {
        ... on OrderSummaryType {
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
          placedAt
          items {
            itemId
            quantity
            itemPrice
            subtotal
          }
        }
        ... on PromoCodeNotFound {
          __typename
          promoCodeId
        }
        ... on PromoCodeUsageLimitReached {
          __typename
          maxUsageCount
        }
        ... on PromoCodeNotEligible {
          __typename
          minOrderValue
          itemsTotal
        }
        ... on AddressIdNotFound {
          __typename
          addressId
        }
        ... on DeliveryUnavailableForAddress {
          __typename
          restaurantId
          pinCode
        }
        ... on RestaurantNotOpen {
          __typename
          restaurantId
          dayOfWeek
        }
        ... on RestaurantClosed {
          __typename
          restaurantId
        }
        ... on CartIsEmpty {
          __typename
          cartId
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
        ... on UserNotRestaurantOwner {
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
        ... on OrderSummaryType {
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
          placedAt
          items {
            itemId
            quantity
            itemPrice
            subtotal
          }
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
        ... on UserNotRestaurantOwner {
          __typename
          userId
        }
      }
    }
    """


class BaseTodayRestaurantOrdersTestCase(GraphQLBaseTestCase):
    QUERY = """
    query TodayRestaurantOrders($params: GetTodayRestaurantOrdersInputParams!) {
      todayRestaurantOrders(params: $params) {
        ... on OrderSummariesType {
          __typename
          orderSummaries {
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
            items {
              itemId
              quantity
              itemPrice
              subtotal
            }
          }
        }
        ... on UserNotRestaurantOwner {
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
        ... on OrderNotFound {
          __typename
          orderId
        }
        ... on OrderNotOwnedByUser {
          __typename
          orderId
        }
        ... on OrderCancellationWindowExpired {
          __typename
          orderId
          minutes
        }
        ... on OrderCancellationNotAllowed {
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
        ... on OrderNotFound {
          __typename
          orderId
        }
        ... on OrderCancellationNotAllowed {
          __typename
          orderId
        }
      }
    }
    """
