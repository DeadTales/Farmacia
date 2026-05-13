from postgrest.exceptions import APIError

from Core.Address.CatStateManager import CatStateManager
from Core.Response import Response
from Models.Address.CatCity import CatCity
from Services.Address.CatCityRepository import CatCityRepository


class CatCityManager:
    @staticmethod
    def get_all_cities():
        try:
            data = CatCityRepository.get_all()
            if not data:
                return Response(data=[], message="No hay ciudades", status=204)
            return Response(data=[CatCity.from_dict(item) for item in data], message="Consulta exitosa de ciudades", status=200)
        except APIError as e:
            raise APIError(e)

    @staticmethod
    def get_or_create(name: str, state_name: str):
        if not name:
            raise ValueError("No hay municipio o ciudad")
        state = CatStateManager.get_or_create(state_name)
        data = CatCityRepository.get_by_name_and_state(name.strip(), state.get_state_id())
        if data:
            return CatCity.from_dict(data)
        created = CatCityRepository.create({"name": name.strip(), "state_id": state.get_state_id()})
        city = CatCity.from_dict(created[0] if isinstance(created, list) else created)
        city.set_cat_state(state)
        return city
