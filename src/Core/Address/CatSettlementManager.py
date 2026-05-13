from postgrest.exceptions import APIError

from Core.Address.CatCityManager import CatCityManager
from Core.Response import Response
from Models.Address.CatSettlement import CatSettlement
from Services.Address.CatSettlementRepository import CatSettlementRepository


class CatSettlementManager:
    @staticmethod
    def get_all_settlements():
        try:
            data = CatSettlementRepository.get_all()
            if not data:
                return Response(data=[], message="No hay colonias", status=204)
            return Response(data=[CatSettlement.from_dict(item) for item in data], message="Consulta exitosa de colonias", status=200)
        except APIError as e:
            raise APIError(e)

    @staticmethod
    def get_or_create(name: str, city_name: str, state_name: str):
        if not name:
            raise ValueError("No hay colonia")
        city = CatCityManager.get_or_create(city_name, state_name)
        data = CatSettlementRepository.get_by_name_and_city(name.strip(), city.get_city_id())
        if data:
            return CatSettlement.from_dict(data)
        created = CatSettlementRepository.create({"name": name.strip(), "city_id": city.get_city_id()})
        settlement = CatSettlement.from_dict(created[0] if isinstance(created, list) else created)
        settlement.set_cat_city(city)
        return settlement
