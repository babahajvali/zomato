import json
import re

import jwt
from django.conf import settings
from django.http import JsonResponse


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user_id = None

        if not request.path.startswith("/graphql"):
            return self.get_response(request)

        if request.method == "GET" and settings.DEBUG:
            return self.get_response(request)

        if request.method == "OPTIONS":
            return self.get_response(request)

        if self._is_public_operation(request):
            return self.get_response(request)

        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return JsonResponse(
                {"errors": [{"message": "Authentication required"}]},
                status=401,
            )

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {"errors": [{"message": "Token has expired. Please login again."}]},
                status=401,
            )
        except jwt.InvalidTokenError:
            return JsonResponse(
                {"errors": [{"message": "Invalid token"}]},
                status=401,
            )

        request.user_id = payload.get("user_id")
        return self.get_response(request)

    @staticmethod
    def _is_public_operation(request):
        try:
            body = request.body
            if not body:
                return False

            data = json.loads(body.decode("utf-8"))
            operation_name = data.get("operationName", "")
            query = data.get("query", "")

            public_operations = {
                "introspectionquery",
                "userlogin",
            }

            if operation_name.lower() in public_operations:
                return True

            query_lower = query.lower().strip()

            public_mutations = {
                "userlogin",
            }

            for mutation in public_mutations:
                if "mutation" in query_lower and mutation in query_lower:
                    return True

            introspection_pattern = re.compile(
                r"\b(__schema|__type)\s*[({]",
                re.IGNORECASE,
            )
            if introspection_pattern.search(query):
                return True

            return False

        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            return False
