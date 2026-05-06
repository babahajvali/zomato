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

        ... on PromoCodeExpired {
          __typename
          code
        }

        ... on PromoCodeNotYetValid {
          __typename
          code
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

        ... on CustomerCartNotFound {
          __typename
          customerId
        }

        ... on MenuItemsUnavailable {
          __typename
          unavailableItemIds
        }
      }
    }
    """


class BasePlaceScheduledOrderTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation PlaceScheduledOrder($params: PlaceScheduledOrderInputParams!) {
      placeScheduledOrder(params: $params) {
        ... on ScheduledOrderSummaryType {
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
          scheduledFor
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

        ... on PromoCodeExpired {
          __typename
          code
        }

        ... on PromoCodeNotYetValid {
          __typename
          code
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

        ... on ScheduledTimeTooSoon {
          __typename
          scheduledFor
        }

        ... on RestaurantNotOpenAtScheduledTime {
          __typename
          restaurantId
          scheduledFor
        }

        ... on CartIsEmpty {
          __typename
          cartId
        }

        ... on CustomerCartNotFound {
          __typename
          customerId
        }

        ... on MenuItemsUnavailable {
          __typename
          unavailableItemIds
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
    query UserOrders($params: GetUserOrdersInputParams!) {
      userOrders(params: $params) {
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


class BaseUserScheduledOrdersTestCase(GraphQLBaseTestCase):
    QUERY = """
    query UserScheduledOrders($params: GetUserScheduledOrdersInputParams!) {
      userScheduledOrders(params: $params) {
        ... on ScheduledOrderSummariesType {
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
            scheduledFor
            items {
              itemId
              quantity
              itemPrice
              subtotal
            }
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


class BaseTodayRestaurantScheduledOrdersTestCase(GraphQLBaseTestCase):
    QUERY = """
    query TodayRestaurantScheduledOrders($params: GetTodayRestaurantScheduledOrdersInputParams!) {
      todayRestaurantScheduledOrders(params: $params) {
        ... on ScheduledOrderSummariesType {
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
            scheduledFor
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
        ... on OrderAlreadyCancelled {
        __typename
        orderId
        }
      }
    }
    """
