import copy

from Models.Address.CatCity import CatCity

class CatSettlement:

    def __init__(self, settlement_id: int = None, name: str = None, 
                 cat_ciry: CatCity = None):
        self.settlement_id = settlement_id
        self.name = name
        self.cat_city = cat_ciry

    @classmethod
    def from_dict(cls, data: dict):
        pass

    def set_settlement_id(self, settlement_id: int):
        self.settlement_id = settlement_id
    
    def set_name(self, name: str):
        self.name = name

    def set_cat_city(self, cat_city: CatCity):
        self.cat_city = cat_city

    def get_settlement_id(self):
        return copy.copy(self.settlement_id)
    
    def get_name(self):
        return copy.copy(self.name)
    
    def get_cat_city(self):
        return copy.copy(self.cat_city)