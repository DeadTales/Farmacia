import copy

from Models.Product import Product

class TransactionDetail:

    def __init__(self, detail_id: int = None, amount: int = None, 
                 unit_price: float = None, product: Product = None):

        self.detail_id = detail_id
        self.amount = amount
        self.unit_price = unit_price
        self.product = product

    @classmethod
    def from_dict(cls, data: dict):
        if data:
            return cls(
                detail_id=data.get("detail_id") or data.get("datail_id"),
                amount=data.get("amount"),
                unit_price=data.get("historical_price_unit") or data.get("historical_unit_price"),
                product=Product.from_dict(data.get("product")) if isinstance(data.get("product"), dict) else data.get("product")
            )

    def set_detail_id(self, detail_id: int):
        self.detail_id = detail_id
    
    def set_amount(self, amount: int):
        self.amount = amount
    
    def set_unit_price(self, unit_price: float):
        self.unit_price = unit_price
    
    def set_product(self, product: Product):
        self.product = product

    def get_detail_id(self):
        return copy.copy(self.detail_id)

    def get_amount(self):
        return copy.copy(self.amount)
    
    def get_unit_price(self):
        return copy.copy(self.unit_price)
    
    def get_product(self):
        return copy.copy(self.product)

    def get_subtotal(self):
        return (self.amount or 0) * (self.unit_price or 0)
    
