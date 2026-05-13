from typing import List


class DuplicateEmails(Exception):
    def __init__(self, emails: List[str]):
        self.emails = emails


class EmailAlreadyExists(Exception):
    def __init__(self, emails: List[str]):
        self.emails = emails


class EmailNotFound(Exception):
    # TODO: declared but never raised anywhere — dead exception. Either wire it up or remove.
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
        # TODO: this isn't an f-string and `addresses` is undefined (missing self.) — raises NameError when stringified.
        return "Duplicate addresses found: {', '.join([f'{addr[0]} - {addr[1]}' for addr in addresses])}"


class InvalidCredentials(Exception):
    def __init__(self, email: str):
        self.email = email

    def __str__(self):
        return f"Invalid credentials: {self.email}"