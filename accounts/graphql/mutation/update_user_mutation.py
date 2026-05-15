import graphene

from accounts.exception import custom_exceptions
from accounts.graphql.types.error_types import (
    EmptyUserNameFound,
    NothingToUpdateUserProperties,
    UserNotFound,
)
from accounts.graphql.types.input_types import UpdateUserInputParams
from accounts.graphql.types.response_types import UpdateUserResponse
from accounts.graphql.types.types import UserType
from accounts.interactors.dtos import UpdateUserDTO
from accounts.interactors.user.user_interactor import UserInteractor
from accounts.storages.user_storage import UserStorage
from utils.auth_decorators import require_auth


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        params = UpdateUserInputParams(required=True)

    Output = UpdateUserResponse

    @staticmethod
    @require_auth
    def mutate(root, info, params):
        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        update_user_dto = UpdateUserDTO(
            user_id=params.user_id,
            name=params.name,
            phone_number=params.phone_number,
        )

        try:
            user_dto = interactor.update_user(update_user_dto=update_user_dto)

            return UserType(
                user_id=user_dto.id,
                email=user_dto.email,
                name=user_dto.name,
                phone_number=user_dto.phone_number,
                role=user_dto.role,
            )
        except custom_exceptions.UserNotFound as e:
            return UserNotFound(user_id=e.user_id)
        except custom_exceptions.EmptyUserNameFound as e:
            return EmptyUserNameFound(name=e.name)
        except custom_exceptions.NothingToUpdateUserProperties as e:
            return NothingToUpdateUserProperties(user_id=e.user_id)
