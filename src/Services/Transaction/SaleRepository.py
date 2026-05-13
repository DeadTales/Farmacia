from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class SaleRepository(BaseRepository):
    table_name = "sale"
    pk_column = "sale_id"

    @classmethod
    def get_all(cls):
        try:
            response = db.table(cls.table_name).select(
                "sale_id, date_hour, total_sale, client:client(*), user:profile(nickname, first_name, last_name, user_type:user_type(*))"
            ).execute()
            return response.data if response.data else None
        except APIError as e:
            cls._log_error(e)
            raise

    @classmethod
    def create_sale(cls, data_dict: dict):
        try:
            response = db.table(cls.table_name).insert(data_dict).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise
