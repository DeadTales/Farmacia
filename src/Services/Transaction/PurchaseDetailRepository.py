from postgrest.exceptions import APIError

from Services.BaseRepositoty import BaseRepository
from Services.Connection import db


class PurchaseDetailRepository(BaseRepository):
    table_name = "purchase_detail"
    pk_column = "detail_id"

    @classmethod
    def create_many(cls, details: list[dict]):
        try:
            response = db.table(cls.table_name).insert(details).execute()
            return response.data
        except APIError as e:
            cls._log_error(e)
            raise
