from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class CatSettlementRepository(BaseRepository):
    table_name = "cat_settlement"
    pk_column = "settlement_id"

    @classmethod
    def get_all(cls):
        try:
            response = db.table(cls.table_name).select(
                "*, cat_city:cat_city(*, cat_state:cat_state(*))"
            ).execute()
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error cargando colonias: {e.message}")

    @classmethod
    def get_by_name_and_city(cls, name: str, city_id: int):
        try:
            response = db.table(cls.table_name).select("*, cat_city:cat_city(*, cat_state:cat_state(*))") \
                .ilike("name", name).eq("city_id", city_id).limit(1).execute()
            return response.data[0] if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error buscando colonia: {e.message}")
