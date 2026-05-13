from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class ProductRepository(BaseRepository):
    table_name = "product"
    pk_column = "barcode"

    @classmethod
    def get_all(cls):

        try:
            response = db.table(cls.table_name).select("barcode, name, description, stock, price, category: category(*), mark: mark(*)") \
                        .eq("is_active", True).execute()
            
            return response.data if response.data else None

        except APIError as e:
            print(f"Errror cargando {cls.table_name}: {e.message}")
            raise APIError(e)
    
    @classmethod
    def get_generic(cls):
        try:
            response = db.table(cls.table_name) \
                .select("barcode, name, description, stock, price, category: category(*), mark: mark(*)") \
                .neq("category_id", 1).eq("is_active", True).execute()
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error cargando {cls.table_name}: {e.message}")

    @classmethod
    def get_one(cls, value_id):
        try:
            response = db.table(cls.table_name).select("barcode, name, description, stock, price, category: category(*), mark: mark(*)") \
                        .eq(cls.pk_column, value_id).single().execute()
            
            return response.data if response.data else None

        except APIError as e:
            print(f"Errror cargando {cls.table_name}: {e.message}")
            raise APIError(e)

    @classmethod
    def update_stock(cls, barcode: str, stock: int):
        try:
            response = db.table(cls.table_name).update({"stock": stock}).eq(cls.pk_column, barcode).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error actualizando stock de {cls.table_name}: {e.message}")

    @classmethod
    def update_stock_and_price(cls, barcode: str, stock: int, price: float):
        try:
            response = db.table(cls.table_name).update({"stock": stock, "price": price}).eq(cls.pk_column, barcode).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error actualizando stock y precio de {cls.table_name}: {e.message}")

    @classmethod
    def delete_logic(cls, id_value):
        try:
            response = db.table(cls.table_name).update({"is_active": False})\
                .eq(cls.pk_column, id_value).execute()
            
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error en borrado lógico de {cls.table_name}: {e.message}")
