from dataclasses import dataclass

from account.constants.enums import Role


@dataclass
class CreateUserDTO:
    name: str
    email: str
    phone_number: str
    role: Role


@dataclass
class CreateAddressDTO:
    email: str
    label: str
    full_address: str
    city: str
    pincode: str
    is_default: bool


@dataclass
class UserDTO:
    id: str
    name: str
    email: str
    phone_number: str
    role: Role