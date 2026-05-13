import graphene


class AddressType(graphene.ObjectType):
    # TODO: address_id is int in DTO/PK but exposed here as String — silent coercion. Use Int or ID.
    address_id = graphene.String(required=True)
    full_address = graphene.String(required=True)
    city = graphene.String(required=True)
    pincode = graphene.String(required=True)
    label = graphene.String(required=True)
    is_default = graphene.Boolean(required=True)
    user_id = graphene.String(required=True)

class UserAddressesType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    # TODO: addresses isn't required — resolver always returns a list (possibly empty). Mark required=True to firm up the contract.
    addresses = graphene.List(AddressType)