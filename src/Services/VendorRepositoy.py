from postgrest.exceptions import APIError

from Services.Connection import db
from Services.BaseRepositoty import BaseRepository
from Models.Vendor import Vendor

class VendorRepositoy(BaseRepository):
    table_name = "vendor"
    pk_column = "vendor_id"
    



   