from accounts.exception import custom_exceptions
from accounts.graphql.types.error_types import UserNotFound
from accounts.graphql.types.types import AddressType, UserAddressesType
from accounts.interactors.address.address_interactor import (
    AddressInteractor,
)
from accounts.storages.address_storage import AddressStorage
from accounts.storages.user_storage import UserStorage
from utils.graphql_types import UnauthorizedFound


def get_user_addresses_resolver(root, info):

    user_storage = UserStorage()
    address_storage = AddressStorage()

    interactor = AddressInteractor(
        user_storage=user_storage, address_storage=address_storage
    )

    try:
        user_id = info.context.user_id

        if user_id is None:
            return UnauthorizedFound(context_user_id=user_id)

        result = interactor.get_user_addresses(user_id=user_id)

        user_addresses = [
            AddressType(
                address_id=each.address_id,
                full_address=each.full_address,
                city=each.city,
                pincode=each.pincode,
                is_default=each.is_default,
                label=each.label,
                user_id=each.user_id,
            )
            for each in result
        ]
        return UserAddressesType(user_id=user_id, addresses=user_addresses)

    except custom_exceptions.UserNotFound as e:
        return UserNotFound(user_id=e.user_id)
