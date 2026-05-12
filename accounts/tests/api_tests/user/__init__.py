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


class BaseCreateUserTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation CreateUser($params: CreateUserInputParams!) {
      createUser(params: $params) {
        ... on UserType {
          __typename
          email
          name
          phoneNumber
          role
        }
        ... on EmailAlreadyExists {
          __typename
          emails
        }
        ... on EmptyUserNameFound {
          __typename
          name
        }
      }
    }
    """


class BaseUpdateUserTestCase(GraphQLBaseTestCase):
    QUERY = """
    mutation UpdateUser($params: UpdateUserInputParams!) {
      updateUser(params: $params) {
        ... on UserType {
          __typename
          userId
          email
          name
          phoneNumber
          role
        }
        ... on UserNotFound {
          __typename
          userId
        }
        ... on EmptyUserNameFound {
          __typename
          name
        }
        ... on NothingToUpdateUserProperties {
          __typename
          userId
        }
      }
    }
    """
