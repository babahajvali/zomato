import uuid
import time
from contextlib import contextmanager

from django_redis import get_redis_connection

from utils.exceptions import ResourceLocked

unlock_script = """
                if redis.call("get", KEYS[1]) == ARGV[1] then
                    return redis.call("del", KEYS[1])
                else
                    return 0
                end
                """


@contextmanager
def redis_lock(
    lock_key: str,
    timeout: int = 10,
    retries: int = 3,
    retry_delay: float = 0.2,
):
    redis_client = get_redis_connection("default")
    lock_value = str(uuid.uuid4())
    acquired = False

    for attempt in range(retries):
        acquired = redis_client.set(
            lock_key,
            lock_value,
            nx=True,
            ex=timeout,
        )

        if acquired:
            break

        if attempt < retries - 1:
            time.sleep(retry_delay)

    # TODO: no retry/backoff — first contention fails immediately. Consider optional retries / retry_delay.
    if not acquired:
        raise ResourceLocked(lock_key=lock_key)

    try:
        yield
    finally:
        redis_client.eval(unlock_script, 1, lock_key, lock_value)
