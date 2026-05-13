from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class PurchaseRepository(BaseRepository):
    table_name = "purchase"
    pk_column = "purchase_id"

    @classmethod
    def create_purchase(cls, data_dict: dict):
        try:
            response = db.table(cls.table_name).insert(data_dict).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise
