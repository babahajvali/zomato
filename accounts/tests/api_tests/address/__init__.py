from utils.test_utils import GraphQLBaseTestCase


class BaseGetUserAddressesTestCase(GraphQLBaseTestCase):
    QUERY = """
    query GetUserAddresses {
      userAddresses {
        ... on AddressesType {
          __typename
          addresses {
            addressId
            fullAddress
            city
            pincode
            label
            isDefault
            userId
          }
        }
      }
    }
    """
