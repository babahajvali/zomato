import graphene


class AddressType(graphene.ObjectType):
    address_id = graphene.Int(required=True)
    full_address = graphene.String(required=True)
    city = graphene.String(required=True)
    pincode = graphene.String(required=True)
    label = graphene.String(required=True)
    is_default = graphene.Boolean(required=True)
    user_id = graphene.String(required=True)


class UserAddressesType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    addresses = graphene.List(AddressType, required=True)


class UserLoginType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    email = graphene.String(required=True)
    name = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    role = graphene.String(required=True)
    access_token = graphene.String(required=True)


class UserType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    email = graphene.String(required=True)
    name = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    role = graphene.String(required=True)
