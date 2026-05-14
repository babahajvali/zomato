from orders.adapter.dtos import AddressDTO


class AccountAdapter:
    def __init__(self):
        from accounts.app_interface.service_interface import ServiceInterface

        self.interface = ServiceInterface()

    def get_address_by_id(self, address_id: int, user_id: str) -> AddressDTO:

        return self.interface.get_address_by_id(address_id=address_id, user_id=user_id)
