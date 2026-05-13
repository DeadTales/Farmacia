from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class UserRepository(BaseRepository):
    table_name = "profile"
    pk_column = "nickname"

    @classmethod
    def get_all(cls):
        try:
            response = db.table(cls.table_name).select(
                "nickname, first_name, last_name, user_type: user_type(*)"
            ).execute()
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error cargando usuarios: {e.message}")

    @classmethod
    def get_one(cls, value_id):
        try:
            response = db.table(cls.table_name).select(
                "nickname, first_name, last_name, user_type: user_type(*)"
            ).eq(cls.pk_column, value_id).single().execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error buscando usuario: {e.message}")

    @classmethod
    def get_user_types(cls):
        try:
            response = db.table("user_type").select("*").execute()
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error cargando tipos de usuario: {e.message}")
