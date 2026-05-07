import graphene


class UserLoginInputParams(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
