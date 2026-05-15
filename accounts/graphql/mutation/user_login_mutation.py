from datetime import datetime, timedelta, timezone

import graphene
import jwt

from accounts.exception import custom_exceptions
from accounts.graphql.types.error_types import EmailNotFound, InvalidCredentials
from accounts.graphql.types.input_types import UserLoginInputParams
from accounts.graphql.types.response_types import UserLoginResponse
from accounts.graphql.types.types import UserLoginType
from accounts.interactors.user.user_login_interactor import UserLoginInteractor
from accounts.storages.user_storage import UserStorage
from zomato import settings


class UserLoginMutation(graphene.Mutation):
    class Arguments:
        params = UserLoginInputParams(required=True)

    Output = UserLoginResponse

    @staticmethod
    def mutate(root, info, params):

        user_storage = UserStorage()

        interactor = UserLoginInteractor(user_storage=user_storage)

        try:
            user_dto = interactor.user_login(
                email=params.email, password=params.password
            )

            jwt_token = _generate_access_token(user_id=user_dto.id)

            return UserLoginType(
                user_id=user_dto.id,
                email=user_dto.email,
                name=user_dto.name,
                phone_number=user_dto.phone_number,
                role=user_dto.role,
                access_token=jwt_token,
            )

        except custom_exceptions.EmailNotFound as e:
            return EmailNotFound(email=e.email)
        except custom_exceptions.InvalidCredentials as e:
            return InvalidCredentials(email=e.email)


def _generate_access_token(user_id):
    payload = {
        "user_id": str(user_id),
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token
