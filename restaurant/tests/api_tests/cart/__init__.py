from utils.test_utils import GraphQLBaseTestCase


class BaseUpdateCartItemTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation UpdateCartItem($params: UpdateCartItemInputParams!) {
      updateCartItem(params: $params) {
        ... on CartItemType {
          __typename
          cartId
          cartItemId
          itemPrice
          quantity
          menuItemId
        }
        ... on CartNotFound {
          __typename
          cartId
        }
        ... on InvalidQuantity {
          __typename
          quantity
        }
        ... on MenuItemNotFound {
          __typename
          menuItemId
        }
      }
    }
    """


class BaseRemoveCartItemTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation RemoveCartItem($params: RemoveCartItemInputParams!) {
      removeCartItem(params: $params) {
        ... on RemoveCartItemSuccessType {
          __typename
          cartItemId
          success
        }
        ... on CartItemNotFound {
          __typename
          cartItemId
        }
      }
    }
    """


class BaseClearCartItemsTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation ClearCartItems($params: ClearCartItemsInputParams!) {
      clearCartItems(params: $params) {
        ... on ClearCartItemsSuccessType {
          __typename
          cartId
          success
        }
        ... on CartNotFound {
          __typename
          cartId
        }
      }
    }
    """


class BaseGetCartItemsTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetCartItems($params: GetCartItemsInputParams!) {
      getCartItems(params: $params) {
        ... on CartItemsType {
          __typename
          cartItems {
            cartId
            cartItemId
            itemPrice
            menuItemId
            quantity
          }
        }
        ... on CartNotFound {
          __typename
          cartId
        }
      }
    }
    """
