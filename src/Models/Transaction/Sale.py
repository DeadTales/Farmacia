import copy
from datetime import datetime, timezone

from Models.Client import Client
from Models.User import User
from Models.Transaction.Transaction import Transaction

class Sale (Transaction):
    def __init__(self, transaction_id: str, date_hour: datetime = None,
                 client: Client = None, user: User = None, products: list = None):
        
        super().__init__(transaction_id, date_hour, user, products or [])
        self.client = client
    
    @classmethod
    def from_dict(cls, data:dict):
        if data:
            return cls(
                transaction_id=data.get("sale_id"),
                date_hour=data.get("date_hour"),
                client=Client.from_dict(data.get("client")) if isinstance(data.get("client"), dict) else data.get("client"),
                user=User.from_dict(data.get("user")) if isinstance(data.get("user"), dict) else data.get("user"),
                products=data.get("products") or []
            )

    def set_client(self, client: Client):
        self.client = client
    
    def get_client(self):
        return copy.copy(self.client)
    
    def process_inventory(self): #generate ticket and send email..?
        return super().process_inventory()
    
