from typing import List


class DuplicateEmails(Exception):
    def __init__(self, emails: List[str]):
        self.emails = emails


class EmailAlreadyExists(Exception):
    def __init__(self, emails: List[str]):
        self.emails = emails


class EmptyUserNameFound(Exception):
    def __init__(self, name: str):
        self.name = name


class NothingToUpdateUserProperties(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class EmailNotFound(Exception):
    def __init__(self, email: str):
        self.email = email

    def __str__(self):
        return f"User not found: {self.email}"


class UserNotFound(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class AddressAlreadyExists(Exception):
    def __init__(self, addresses: List[tuple]):
        self.addresses = addresses

    def __str__(self):
        return f"Addresses already exist: {', '.join([f'{addr[0]} - {addr[1]}' for addr in self.addresses])}"


class DuplicateAddresses(Exception):
    def __init__(self, addresses: List[tuple]):
        self.addresses = addresses

    def __str__(self):
        return f"Duplicate addresses found: {', '.join(f'{addr[0]} - {addr[1]}' for addr in self.addresses)}"


class InvalidCredentials(Exception):
    def __init__(self, email: str):
        self.email = email

    def __str__(self):
        return f"Invalid credentials: {self.email}"


class InvalidUsersFound(Exception):
    def __init__(self, user_ids: List[str]):
        self.user_ids = user_ids

    def __str__(self):
        return (
            f"Users not found: {', '.join([f'{user_id}' for user_id in self.user_ids])}"
        )


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
