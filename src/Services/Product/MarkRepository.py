from postgrest.exceptions import APIError

from Services.Connection import db
from Services.BaseRepositoty import BaseRepository
from Models.Product.Mark import Mark

class MarkRepository(BaseRepository):
    table_name = "mark"
    pk_column = "mark_id"

    @classmethod
    def get_all(cls):
        try:
            response = db.table(cls.table_name).select("*, vendor: vendor(*)").execute()
            return response.data if response.data else None
        except APIError as e:
            print(e)
            raise APIError(f"Error cargando {cls.table_name}: {e.message}")
        
    
    @classmethod
    def get_one(cls, value_id):
        try:
            response = db.table(cls.table_name).select("*, vendor: vendor(*)").eq(cls.pk_column, value_id) \
                        .single().execute()
            
            return response.data if response.data else None
        except APIError as e:
            print(e)
            raise APIError(f"Error cargando {cls.table_name}: {e.message}")
        
