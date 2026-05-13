from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class ClientRepository(BaseRepository):
    table_name = "client"
    pk_column = "email"

    @classmethod
    def get_all(cls):
        try:
            response = db.table(cls.table_name).select(
                "*, address:address(*, cat_settlement:cat_settlement(*, cat_city:cat_city(*, cat_state:cat_state(*))))"
            ).execute()
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error cargando clientes: {e.message}")

    @classmethod
    def get_one(cls, value_id):
        try:
            response = db.table(cls.table_name).select(
                "*, address:address(*, cat_settlement:cat_settlement(*, cat_city:cat_city(*, cat_state:cat_state(*))))"
            ).eq(cls.pk_column, value_id).single().execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error buscando cliente: {e.message}")
