import copy

from Models.Product.Category import Category
from Models.Product.Mark import Mark
from Models.Product.Product import Product

class Medicine(Product):
    def __init__(self, barcode:str = None, name:str = None, description:str = None, 
                 stock:int = None, mark: Mark = None, is_active : bool = None, 
                 concentration: str = None, active_ingredient: str = None, 
                 presentation: str = None, prescription: bool = None):
        
        super().__init__(barcode, name, description, 
                         stock, Category(category_id=1, name="Medicamento"), mark, is_active)

        self.concentration = concentration
        self.active_ingredient = active_ingredient
        self.presentation = presentation
        self.prescription = prescription
    
    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        
        product_info: dict = data.get("product", {})
        
        return cls(
            barcode = data.get("barcode"),
            name = product_info.get("name"),
            description = product_info.get("description"),
            stock = product_info.get("stock"),
            mark = Mark.from_dict(product_info.get("mark")),      
            is_active=product_info.get("is_active"),
            
            # Datos de la tabla Medicine
            concentration=data.get("concentration"),
            active_ingredient=data.get("active_ingredient"),
            presentation=data.get("presentation"),
            prescription=data.get("prescription")
        )

    def to_product_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "stock": self.stock,
            "mark_id": self.mark.mark_id if self.mark else None,
            "category_id": 1,
            "is_active": True
        }

    def to_medicine_dict(self):
        return {
            "concentration": self.concentration,
            "active_ingredient": self.active_ingredient,
            "presentation": self.presentation,
            "prescription": self.prescription
        } 

    def set_concentration(self, concentration: str):
        self.concentration = concentration
    
    def set_active_ingredient(self, active_ingredient:str):
        self.active_ingredient = active_ingredient
    
    def set_presentation(self, presentation: str):
        self.presentation = presentation
    
    def set_prescription(self, prescription: bool):
        self.prescription = prescription

    def get_concentration(self):
        return copy.copy(self.concentration)
    
    def get_active_ingredient(self):
        return copy.copy(self.active_ingredient)
    
    def get_presentation(self):
        return copy.copy(self, self.presentation)
    
    def get_prescrption(self):
        return copy.copy(self.prescription)
    
    
    
