from utils.test_utils import GraphQLBaseTestCase


class BaseGetUserAddressesTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetUserAddresses {
      getUserAddresses {
        ... on UserAddressesType {
          __typename
          userId
          addresses {
            addressId
            fullAddress
            city
            pincode
            label
            isDefault
          }
        }
        ... on UserNotFound {
          __typename
          userId
        }
      }
    }
    """
