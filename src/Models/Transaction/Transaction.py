import copy
from datetime import datetime, timezone

from Models.User import User
from Models.Transaction import TransactionDetail

class Transaction:
    def __init__(self, transaction_id: str, date_hour: datetime = None,
                 user: User = None, products: list = None):
        self.transaction_id = transaction_id
        self.date_hour = date_hour
        self.user = user
        self.products = products
    
    @classmethod
    def from_dict(cls, data:dict):
        pass

    def set_transaction_id(self, transaction_id: str):
        self.transaction_id = transaction_id

    def set_date_hour(self, date_hour:datetime):
        self.date_hour = date_hour
    
    def set_user(self, user: User):
        self.user = user
    
    def set_products(self, products: list):
        self.products = products
    
    def get_transaction_id(self):
        return copy.copy(self.transaction_id)
    
    def get_date_hour(self):
        return copy.copy(self.date_hour)
    
    def get_user(self):
        return copy.copy(self.user)
    
    def get_products(self):
        return copy.copy(self.products)
    
    def calculateTotal(self):
        return sum(detail.get_subtotal() for detail in self.products or [])
    
    def addProduct(self, detail: TransactionDetail):
        if self.products is None:
            self.products = []
        current = self.searchDetail(detail.product.barcode)
        if current:
            current.amount = (current.amount or 0) + (detail.amount or 0)
            current.unit_price = detail.unit_price
            return current
        self.products.append(detail)
        return detail

    def searchDetail(self, barcode: str)-> TransactionDetail: #or  -> int:
        for detail in self.products or []:
            if detail.product and detail.product.barcode == barcode:
                return detail
        return None

    def deleteProduct(self, barcode: str):
        if self.products is None:
            return
        self.products = [detail for detail in self.products if not detail.product or detail.product.barcode != barcode]

    def editAmount(self, barcode: str, new_amount: int):
        detail = self.searchDetail(barcode)
        if detail:
            detail.amount = new_amount
        return detail

    def process_inventory(self):
        pass
