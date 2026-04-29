from dataclasses import dataclass

from accounts.constants.enums import Role


@dataclass
class CreateUserDTO:
    id: str
    name: str
    email: str
    phone_number: str
    role: Role


@dataclass
class CreateAddressDTO:
    user_id: str
    label: str
    full_address: str
    city: str
    pincode: str
    is_default: bool


@dataclass
class AddressDTO:
    address_id: int
    full_address: str
    city: str
    pincode: str
    label: str
    is_default: bool
    user_id: str


@dataclass
class UserDTO:
    id: str
    name: str
    email: str
    phone_number: str
    role: Role
