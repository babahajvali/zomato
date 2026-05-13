from dataclasses import dataclass
from typing import Optional

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
class UpdateAddressDTO:
    id: int
    user_id: str
    label: str
    full_address: str
    city: str
    pincode: int
    is_default: bool


@dataclass
class AddressDTO:
    address_id: int
    full_address: str
    city: str
    pincode: int
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
    password: str


@dataclass
class UserCreateDTO:
    name: str
    email: str
    phone_number: str
    role: Role
    password: str


@dataclass
class UpdateUserDTO:
    user_id: str
    name: Optional[str]
    phone_number: Optional[str]


@dataclass
class AddressLookupDTO:
    user_id: str
    label: str
    pincode: int
