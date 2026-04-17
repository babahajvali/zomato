from typing import List


class DuplicateUserEmails(Exception):
    def __init__(self, emails: List[str]):
        self.emails = emails

class AlreadyExistsEmail(Exception):
    def __init__(self, emails: List[str]):
        self.emails = emails


class UserNotFound(Exception):
    def __init__(self, email):
        self.email = email
        super().__init__(f"User not found: {email}")


class AlreadyExistsAddress(Exception):
    def __init__(self, addresses):
        self.addresses = addresses
        super().__init__(f"Addresses already exist: {', '.join([f'{addr[0]} - {addr[1]}' for addr in addresses])}")


class DuplicateAddresses(Exception):
    def __init__(self, addresses):
        self.addresses = addresses
        super().__init__(f"Duplicate addresses found: {', '.join([f'{addr[0]} - {addr[1]}' for addr in addresses])}")
