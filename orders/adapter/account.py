from orders.adapter.dtos import AddressDTO


class AccountAdapter:
    @property
    def interface(self):

        from accounts.app_interface.service_interface import ServiceInterface

        return ServiceInterface()

    def get_address_by_id(self, address_id: int) -> AddressDTO:

        return self.interface.get_address_by_id(address_id)
