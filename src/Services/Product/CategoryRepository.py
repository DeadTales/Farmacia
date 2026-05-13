from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db

class CategoryRepository(BaseRepository):
    table_name = "category"
    pk_column = "category_id"

    @classmethod
    def get_generic(cls):
        try:
            response = db.table("category").select("*").neq(cls.pk_column, 1).execute()
            return response.data
        except APIError as e:
            print(f"Errror cargando {cls.table_name}: {e.message}")
            raise APIError(e)