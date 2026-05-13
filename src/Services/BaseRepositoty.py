from Services.Connection import db
from postgrest.exceptions import APIError

class BaseRepository:
    table_name = ""
    pk_column = "id"

    @classmethod
    def get_all(cls):
        try:
            response = db.table(cls.table_name).select("*").execute()
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error cargando {cls.table_name}: {e.message}")

    @classmethod
    def get_one(cls, value_id):
        try:
            response = db.table(cls.table_name).select("*").eq(cls.pk_column, value_id).single().execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error buscando en {cls.table_name}: {e.message}")

    @classmethod
    def create(cls, data_dict: dict):
        try:
            response = db.table(cls.table_name).insert(data_dict).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error creando en {cls.table_name}: {e.message}")

    @classmethod
    def update(cls, value_id, data_dict: dict):
        try:
            response = db.table(cls.table_name).update(data_dict).eq(cls.pk_column, value_id).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error actualizando {cls.table_name}: {e.message}")
    
    @classmethod
    def delete(cls, value_id):
        try:
            response = db.table(cls.table_name).delete().eq(cls.pk_column, value_id).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error eliminando {cls.table_name}: {e.message}")

    @staticmethod
    def _log_error(e):
        print(f"Database Error: {e.message}")