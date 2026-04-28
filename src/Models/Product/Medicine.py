import copy

from Models.Product.Product import Product


class Medicine(Product):
    def __init__(self, concentration: str, active_ingredient:str,
                 presentation: str, prescription: bool):
        
        self.concentration = concentration
        self.active_ingredient = active_ingredient
        self.presentation = presentation
        self.prescription = prescription
    
    @classmethod
    def from_dict(cls, data: dict):
        pass

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
    
    
    