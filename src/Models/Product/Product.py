import copy

from Models.Product.Category import Category
from Models.Product.Mark import Mark

class  Product:
    def __init__(self, barcode: str, name: str,
                 description: str, stock: int, 
                category: Category, mark: Mark):
        self.barcode = barcode
        self.name = name
        self.description = description
        self.stock = stock
        self.category = category
        self.mark = mark
    
    @classmethod
    def from_dict(cls, data: dict):
        if data:
            return cls (
               barcode=data.get("barcode"),
               name=data.get("name"),
               description=data.get("description"),
               stock=data.get("stock"),
               category=data.get("category"), 
               mark = data.get("mark"),
            )
    
    def to_dict(self):
        return {
            "barcode": self.barcode,
            "name": self.name,
            "description": self.description,
            "stock": self.stock,
            "category": self.category,
            "mark": self.mark
        }
            
    
    def set_barcode(self, barcode: str):
        self.barcode = barcode

    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.description = description

    def set_stock(self, stock: int):
        self.stock = stock
    
    def set_category(self, category: str):
        self.category = category

    def get_barcode(self):
        return copy.copy(self.barcode)
    
    def get_description(self):
        return copy.copy(self.description)
    
    def get_stock(self):
        return copy.copy(self.stock)
    
    def get_category(self):
        return copy.copy(self.category)
    
    def addStock(self, value: int):
        self.stock += value

    def subtractStock(self, value: int):
        self.stock -= value
    
    
