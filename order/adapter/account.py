from account.app_interface.service_interface import ServiceInterface
from order.adapter.dtos import AddressDTO


class AccountAdapter:
    @property
    def interface(self):

        return ServiceInterface()

    def get_address_by_id(self, address_id: int) -> AddressDTO | None:
        address_dto = self.interface.get_address_by_id(address_id)

        if address_dto is None:
            return None
        return address_dto
