import graphene


class UserNotFound(graphene.ObjectType):
    user_id = graphene.String(required=True)


class InvalidCredentials(graphene.ObjectType):
    email = graphene.String(required=True)


class EmailNotFound(graphene.ObjectType):
    email = graphene.String(required=True)


class EmailAlreadyExists(graphene.ObjectType):
    emails = graphene.List(graphene.String, required=True)


class EmptyUserNameFound(graphene.ObjectType):
    name = graphene.String(required=True)


class NothingToUpdateUserProperties(graphene.ObjectType):
    user_id = graphene.String(required=True)


class AddressAlreadyExists(graphene.ObjectType):
    label = graphene.String(required=True)
    pincode = graphene.String(required=True)
