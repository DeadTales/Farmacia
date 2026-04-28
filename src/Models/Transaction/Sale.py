import copy
from datetime import datetime, timezone

from Models.Client import Client
from Models.User import User
from Models.Transaction.Transaction import Transaction

class Sale (Transaction):
    def __init__(self, transaction_id: str, date_hour: datetime = None,
                 client: Client = None, user: User = None, products: list = None):
        
        super.__init__(transaction_id, date_hour, user, products)
        self.client = client
    
    @classmethod
    def from_dict(cls, data:dict):
        pass

    def set_client(self, cliet: Client):
        self.client = self.client
    
    def get_client(self):
        return copy.copy(self.client)
    
    def process_inventory(self): #generate ticket and send email..?
        return super().process_inventory()
    