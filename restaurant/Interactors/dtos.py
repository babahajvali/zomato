from dataclasses import dataclass


@dataclass
class CreateRestaurantDTO:
    name: str
    owner_email: str
    description: str
    cuisine_type: str
    address: str
    pin_code: str
    is_veg_only: bool
    is_active: bool
