from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class MedicineRepository(BaseRepository):
    table_name = "medicine"
    pk_column = "barcode"

    @classmethod
    def get_all(cls):

        try:
            response = db.table(cls.table_name).select(
                    "*, "
                    "product:product!inner("
                        "name, description, stock, is_active, "
                        "mark:mark(*)"
                    ")"
            ).eq("product.is_active", True).execute()
            
            return response.data if response.data else None

        except APIError as e:
            print(f"Errror cargando {cls.table_name}: {e.message}")
            raise APIError(e)
        

    @classmethod
    def get_one(cls, value_id):
        try:
            response = db.table(cls.table_name).select(
                "*, "
                "product:product!inner("
                    "name, description, stock, is_active, "
                    "mark: mark(*)"
                ")"
            ).eq("product.is_active", True).eq(cls.pk_column, value_id).single().execute()
            
            return response.data if response.data else None

        except APIError as e:
            print(f"Errror cargando {cls.table_name}: {e.message}")
            raise APIError(e)

    @classmethod
    def delete_logic(cls, id_value):
        try:
            response = db.table("product").update({"is_active": False})\
                .eq(cls.pk_column, id_value).execute()
            
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise APIError(f"Error en borrado lógico de {cls.table_name}: {e.message}")