from typing import List

from account.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from account.interactors.dtos import CreateAddressDTO
from account.models import User, Address


class AddressStorage(AddressStorageInterface):
    def create_bulk_addresses(self, addresses_dto: List[CreateAddressDTO]):
        addresses = []
        emails = [dto.email for dto in addresses_dto]
        users = User.objects.filter(email__in=emails)

        user_map = {user.email: user for user in users}

        for dto in addresses_dto:
            address = Address(
                user=user_map[dto.email],
                label=dto.label,
                full_address=dto.full_address,
                city=dto.city,
                pin_code=dto.pincode,
                is_default=dto.is_default,
            )
            addresses.append(address)

        created_addresses = Address.objects.bulk_create(addresses)

        return created_addresses

    def get_existing_addresses(
        self, emails: List[str], labels: List[str]
    ) -> List[tuple]:
        return list(
            Address.objects.filter(
                user__email__in=emails, label__in=labels
            ).values_list("user__email", "label")
        )
