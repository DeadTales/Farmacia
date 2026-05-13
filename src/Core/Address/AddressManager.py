from postgrest.exceptions import APIError

from Core.Address.CatSettlementManager import CatSettlementManager
from Core.Response import Response
from Models.Address.Address import Address
from Services.AddressRepository import AddressRepository


class AddressManager:
    @staticmethod
    def get_by_client(client_id: str):
        try:
            data = AddressRepository.get_by_client(client_id)
            return Response(data=Address.from_dict(data) if data else None, message="Consulta exitosa de direccion", status=200)
        except APIError as e:
            raise APIError(e)

    @staticmethod
    def save_for_client(client_id: str, address_data: dict):
        if not address_data or not any([
            address_data.get("street"),
            address_data.get("external_number"),
            address_data.get("internal_number"),
            address_data.get("settlement"),
        ]):
            return None

        settlement = CatSettlementManager.get_or_create(
            address_data.get("settlement"),
            address_data.get("city"),
            address_data.get("state"),
        )
        AddressRepository.delete_by_client(client_id)
        created = AddressRepository.create({
            "street": address_data.get("street"),
            "external_number": address_data.get("external_number"),
            "internal_number": address_data.get("internal_number"),
            "client_id": client_id,
            "settlement_id": settlement.get_settlement_id(),
        })
        return Address.from_dict(created[0] if isinstance(created, list) else created)

    @staticmethod
    def delete_by_client(client_id: str):
        try:
            return Response(data=AddressRepository.delete_by_client(client_id), message="Direccion eliminada", status=200)
        except APIError as e:
            raise APIError(e)
