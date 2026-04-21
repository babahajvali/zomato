from dataclasses import dataclass


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
class DeliveryZoneDTO:
    delivery_zone_id: int
    restaurant_id: str
    pin_code: str
    delivery_fee: float
    estimated_delivery_mins: int
