from postgrest.exceptions import APIError

from Core.Response import Response
from Models.Address.CatState import CatState
from Services.Address.CatStateRepository import CatStateRepository


class CatStateManager:
    @staticmethod
    def get_all_states():
        try:
            data = CatStateRepository.get_all()
            if not data:
                return Response(data=[], message="No hay estados", status=204)
            return Response(data=[CatState.from_dict(item) for item in data], message="Consulta exitosa de estados", status=200)
        except APIError as e:
            raise APIError(e)

    @staticmethod
    def get_or_create(name: str):
        if not name:
            raise ValueError("No hay estado")
        data = CatStateRepository.get_by_name(name.strip())
        if data:
            return CatState.from_dict(data)
        created = CatStateRepository.create({"name": name.strip()})
        return CatState.from_dict(created[0] if isinstance(created, list) else created)
