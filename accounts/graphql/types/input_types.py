import graphene


class UserLoginInputParams(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class CreateUserInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    role = graphene.String(required=True)
    password = graphene.String(required=True)


class UpdateUserInputParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)
    name = graphene.String()
    phone_number = graphene.String()
