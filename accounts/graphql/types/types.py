import graphene


class AddressType(graphene.ObjectType):
    address_id = graphene.String(required=True)
    full_address = graphene.String(required=True)
    city = graphene.String(required=True)
    pincode = graphene.String(required=True)
    label = graphene.String(required=True)
    is_default = graphene.Boolean(required=True)
    user_id = graphene.String(required=True)

class UserAddressesType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    addresses = graphene.List(AddressType)