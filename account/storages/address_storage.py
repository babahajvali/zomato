from typing import List

from account.interactors.storage_interface.address_storage_interface import AddressStorageInterface
from account.interactors.dtos import CreateAddressDTO
from account.models import User, Address
from account.exception.custom_exceptions import UserNotFound


class AddressStorage(AddressStorageInterface):

    def create_bulk_addresses(self, addresses_dto: List[CreateAddressDTO]):
        addresses = []
        
        for dto in addresses_dto:
            try:
                user = User.objects.get(email=dto.email)
            except User.DoesNotExist:
                raise UserNotFound(email=dto.email)
            
            address = Address(
                user=user,
                label=dto.label,
                full_address=dto.full_address,
                city=dto.city,
                pin_code=dto.pincode,
                is_default=dto.is_default,
            )
            addresses.append(address)

        created_addresses = Address.objects.bulk_create(addresses)

        return created_addresses

    def get_existing_addresses(self, emails: List[str], labels: List[str]) -> List[tuple]:
        return list(Address.objects.filter(
            user__email__in=emails,
            label__in=labels
        ).values_list('user__email', 'label'))
