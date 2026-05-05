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
    def get_one(cls, id_value):
        try:
            response = db.table(cls.table_name).select("*").eq(cls.pk_column, id_value).single().execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error buscando en {cls.table_name}: {e.message}")

    @classmethod
    def create(cls, data_dict):
        try:
            response = db.table(cls.table_name).insert(data_dict).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error creando en {cls.table_name}: {e.message}")

    @classmethod
    def update(cls, id_value, data_dict):
        try:
            response = db.table(cls.table_name).update(data_dict).eq(cls.pk_column, id_value).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error actualizando {cls.table_name}: {e.message}")
    
    @classmethod
    def delete(cls, id_value):
        try:
            reponse = db.table(cls.table_name).delete().eq(cls.pk_column, id_value).execute()
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error eliminando {cls.table_name}: {e.message}")

    @staticmethod
    def _log_error(e):
        print(f"Database Error: {e.message}")