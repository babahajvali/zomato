from typing import List, Optional

from django.db.models import Q

from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.exception.custom_exceptions import UserNotFound
from accounts.interactors.dtos import CreateAddressDTO, AddressDTO
from accounts.models import Address, User


class AddressStorage(AddressStorageInterface):
    @staticmethod
    def _convert_to_address_dto(address_obj: Address) -> AddressDTO:
        return AddressDTO(
            address_id=address_obj.pk,
            label=address_obj.label,
            user_id=address_obj.user.id,
            full_address=address_obj.full_address,
            city=address_obj.city,
            pincode=address_obj.pin_code,
            is_default=address_obj.is_default,
        )

    def create_bulk_addresses(self, address_dtos: List[CreateAddressDTO]):
        addresses = []
        user_ids = [dto.user_id for dto in address_dtos]
        users = User.objects.filter(id__in=user_ids)
        user_map = {str(user.id): user for user in users}

        for dto in address_dtos:
            if dto.user_id not in user_map:
                raise UserNotFound(user_id=dto.user_id)
            address = Address(
                user=user_map[dto.user_id],
                label=dto.label,
                full_address=dto.full_address,
                city=dto.city,
                pin_code=dto.pincode,
                is_default=dto.is_default,
            )
            addresses.append(address)

        created_addresses = Address.objects.bulk_create(addresses)

        return created_addresses

    def get_existing_addresses(self, user_label_pairs: List[tuple]) -> List[tuple]:
        query = Q()

        for user_id, label in user_label_pairs:
            query |= Q(user_id=user_id, label=label)

        return list(Address.objects.filter(query).values_list("user_id", "label"))

    def get_address_by_id(self, address_id: int) -> Optional[AddressDTO]:
        address_obj = Address.objects.filter(id=address_id).first()

        if address_obj is None:
            return None
        return self._convert_to_address_dto(address_obj=address_obj)

    def get_user_addresses(self, user_id: str) -> List[AddressDTO]:
        address_objs = Address.objects.filter(user_id=user_id)

        return [
            self._convert_to_address_dto(address_obj=address_obj)
            for address_obj in address_objs
        ]
