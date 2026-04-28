import copy
from datetime import datetime

from Models.User import User
from Models.Vendor import Vendor
from Models.Transaction.Transaction import Transaction

class Purchase(Transaction):
    def __init__(self, transaction_id: str, date_hour: datetime = None,
                 vendor: Vendor = None, user: User = None, products: list = None):
        
        super.__init__(transaction_id, date_hour, user, products)
        self.vendor = vendor

    @classmethod
    def from_dict(cls, dat: dict):
        pass
    
    def set_vendor(self, vendor: Vendor):
        self.vendor = vendor
    
    def get_vendor(self):
        return self.vendor
    
    def process_inventory(self): #generate purchase order and send email
        return super().process_inventory()
    