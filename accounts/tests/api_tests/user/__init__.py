from utils.test_utils import GraphQLBaseTestCase


class BaseUserLoginTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation UserLogin($params: UserLoginInputParams!) {
      userLogin(params: $params) {
        ... on UserLoginType {
          __typename
          accessToken
          email
          name
          phoneNumber
          role
          userId
        }

        ... on InvalidCredentials {
          __typename
          email
        }

        ... on EmailNotFound {
          __typename
          email
        }
      }
    }
    """
