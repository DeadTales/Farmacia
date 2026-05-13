from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class CatCityRepository(BaseRepository):
    table_name = "cat_city"
    pk_column = "city_id"

    @classmethod
    def get_all(cls):
        try:
            response = db.table(cls.table_name).select("*, cat_state:cat_state(*)").execute()
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error cargando ciudades: {e.message}")

    @classmethod
    def get_by_name_and_state(cls, name: str, state_id: int):
        try:
            response = db.table(cls.table_name).select("*, cat_state:cat_state(*)") \
                .ilike("name", name).eq("state_id", state_id).limit(1).execute()
            return response.data[0] if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error buscando ciudad: {e.message}")
