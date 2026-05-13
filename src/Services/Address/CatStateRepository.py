from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class CatStateRepository(BaseRepository):
    table_name = "cat_state"
    pk_column = "state_id"

    @classmethod
    def get_by_name(cls, name: str):
        try:
            response = db.table(cls.table_name).select("*").ilike("name", name).limit(1).execute()
            return response.data[0] if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error buscando estado: {e.message}")
