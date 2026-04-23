from account.exception import custom_exceptions
from account.graphql.types.error_types import UserNotFound
from account.graphql.types.types import AddressType, UserAddressesType
from account.interactors.address.get_user_addresses_interactor import (
    GetUserAddressesInteractor,
)
from account.storages.address_storage import AddressStorage
from account.storages.user_storage import UserStorage


def get_user_addresses_resolver(root, info):

    user_storage = UserStorage()
    address_storage = AddressStorage()

    interactor = GetUserAddressesInteractor(
        user_storage=user_storage, address_storage=address_storage
    )

    try:
        user_id = info.context.user_id
        result = interactor.get_user_addresses(user_id=user_id)

        user_addresses = [
            AddressType(
                address_id=each.address_id,
                full_address=each.full_address,
                city=each.city,
                pincode=each.pincode,
                is_default=each.is_default,
                label=each.label,
            )
            for each in result
        ]
        return UserAddressesType(user_id=user_id, addresses=user_addresses)

    except custom_exceptions.UserNotFound as e:
        return UserNotFound(user_id=e.user_id)
