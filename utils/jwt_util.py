import jwt
from django.conf import settings


# TODO: No exp/iat in payload — tokens never expire. Also why is role hardcoded to "user"?
def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "role": "user",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
