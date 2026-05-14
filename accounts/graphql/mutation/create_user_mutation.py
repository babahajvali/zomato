import graphene

from accounts.constants.enums import Role
from accounts.exception import custom_exceptions
from accounts.graphql.types.error_types import EmailAlreadyExists, EmptyUserNameFound
from accounts.graphql.types.input_types import CreateUserInputParams
from accounts.graphql.types.response_types import CreateUserResponse
from accounts.graphql.types.types import UserType
from accounts.interactors.dtos import UserCreateDTO
from accounts.interactors.user.user_interactor import UserInteractor
from accounts.storages.user_storage import UserStorage


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        params = CreateUserInputParams(required=True)

    Output = CreateUserResponse

    @staticmethod
    def mutate(root, info, params):
        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        create_user_dto = UserCreateDTO(
            name=params.name,
            email=params.email,
            phone_number=params.phone_number,
            role=Role(params.role),
            password=params.password,
        )

        try:
            user_dto = interactor.create_user(create_user_dto=create_user_dto)

            return UserType(
                user_id=user_dto.id,
                email=user_dto.email,
                name=user_dto.name,
                phone_number=user_dto.phone_number,
                role=user_dto.role,
            )
        except custom_exceptions.EmailAlreadyExists as e:
            return EmailAlreadyExists(emails=e.emails)
        except custom_exceptions.EmptyUserNameFound as e:
            return EmptyUserNameFound(name=e.name)
