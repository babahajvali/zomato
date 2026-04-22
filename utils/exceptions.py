class ResourceLocked(Exception):
    def __init__(self, lock_key: str):
        self.lock_key = lock_key

    def __str__(self):
        return str(self.lock_key)
