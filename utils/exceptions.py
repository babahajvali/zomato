class ResourceLocked(Exception):
    def __init__(self, lock_key: str):
        self.lock_key = lock_key

    def __str__(self):
        return str(self.lock_key)


class AddressNotBelongsToUser(Exception):
    def __init__(self, address_id: int, user_id: str):
        self.address_id = address_id
        self.user_id = user_id

    def __str__(self):
        return f"This {self.address_id} Address Id not belongs to user, {self.user_id}"


class AddressNotFound(Exception):
    def __init__(self, address_id: int):
        self.address_id = address_id

    def __str__(self):
        return f"Invalid address {self.address_id}"
