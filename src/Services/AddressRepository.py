from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class AddressRepository(BaseRepository):
    table_name = "address"
    pk_column = "address_id"

    @classmethod
    def get_all(cls):
        try:
            response = db.table(cls.table_name).select(
                "*, cat_settlement:cat_settlement(*, cat_city:cat_city(*, cat_state:cat_state(*)))"
            ).execute()
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error cargando direcciones: {e.message}")

    @classmethod
    def get_by_client(cls, client_id: str):
        try:
            response = db.table(cls.table_name).select(
                "*, cat_settlement:cat_settlement(*, cat_city:cat_city(*, cat_state:cat_state(*)))"
            ).eq("client_id", client_id).limit(1).execute()
            return response.data[0] if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error buscando direccion: {e.message}")

    @classmethod
    def delete_by_client(cls, client_id: str):
        try:
            response = db.table(cls.table_name).delete().eq("client_id", client_id).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error eliminando direccion: {e.message}")
