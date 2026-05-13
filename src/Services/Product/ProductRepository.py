from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class ProductRepository(BaseRepository):
    table_name = "product"
    pk_column = "barcode"

    @classmethod
    def get_all(cls):

        try:
            response = db.table(cls.table_name).select("name, description, stock, category: category(*), mark: mark(*)") \
                        .eq("is_active", 1).execute()
            
            return response if response else None

        except APIError as e:
            print(f"Errror cargando {cls.table_name}: {e.message}")
            raise APIError(e)

    @classmethod
    def get_one(cls, value_id):
        try:
            response = db.table(cls.table_name).select("name, description, stock, category: category(*), mark: mark(*)") \
                        .eq(cls.pk_column, value_id).single().execute()
            
            return response if response else None

        except APIError as e:
            print(f"Errror cargando {cls.table_name}: {e.message}")
            raise APIError(e)

    