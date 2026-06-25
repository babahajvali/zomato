import graphene

from accounts.exception import custom_exceptions
from accounts.graphql.types.error_types import AddressAlreadyExists, UserNotFound
from accounts.graphql.types.input_types import CreateAddressInputParams
from accounts.graphql.types.response_types import CreateAddressResponse
from accounts.graphql.types.types import AddressType
from accounts.interactors.address.address_interactor import AddressInteractor
from accounts.interactors.dtos import CreateAddressDTO
from accounts.storages.address_storage import AddressStorage
from accounts.storages.user_storage import UserStorage
from utils.auth_decorators import require_auth


class CreateAddressMutation(graphene.Mutation):
    class Arguments:
        params = CreateAddressInputParams(required=True)

    Output = CreateAddressResponse

    @staticmethod
    @require_auth
    def mutate(root, info, params):
        user_storage = UserStorage()
        address_storage = AddressStorage()
        interactor = AddressInteractor(
            user_storage=user_storage, address_storage=address_storage
        )

        create_address_dto = CreateAddressDTO(
            user_id=info.context.user_id,
            label=params.label,
            full_address=params.full_address,
            city=params.city,
            pincode=params.pincode,
            is_default=params.is_default or False,
        )

        try:
            address_dto = interactor.create_address(
                create_address_dto=create_address_dto
            )

            return AddressType(
                address_id=address_dto.address_id,
                full_address=address_dto.full_address,
                city=address_dto.city,
                pincode=address_dto.pincode,
                label=address_dto.label,
                is_default=address_dto.is_default,
                user_id=address_dto.user_id,
            )
        except custom_exceptions.UserNotFound as e:
            return UserNotFound(user_id=e.user_id)
        except custom_exceptions.AddressAlreadyExists as e:
            label, pincode = e.addresses[0]
            return AddressAlreadyExists(label=label, pincode=str(pincode))
