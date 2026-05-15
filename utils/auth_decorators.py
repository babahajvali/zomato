from functools import wraps

from utils.graphql_types import UnauthorizedFound


def require_auth(mutate_fn):
    """Block a mutation from running when the request has no authenticated user.

    Defense-in-depth: the JWT middleware already returns 401 for missing/invalid
    tokens, but this guards against bugs in middleware's public-operation
    detection and any future middleware change.

    Apply BEFORE @staticmethod so the wrapper sees the real function:

        @staticmethod
        @require_auth
        def mutate(root, info, params):
            ...

    The Output union of the mutation MUST include `UnauthorizedFound`
    from utils.graphql_types.
    """

    @wraps(mutate_fn)
    def wrapper(root, info, *args, **kwargs):
        user_id = getattr(info.context, "user_id", None)
        if not user_id:
            return UnauthorizedFound(context_user_id=None)
        return mutate_fn(root, info, *args, **kwargs)

    return wrapper
