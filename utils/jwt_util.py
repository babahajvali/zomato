import jwt
from django.conf import settings


def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "role": "user",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
