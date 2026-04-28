import copy
from Models.Address.CatState import CatState

class CatCity:
    def __init__(self, city_id: int = None, name:str = None, 
                 cat_state: CatState = None):
        self.city_id = city_id
        self.name = name
        self.cat_state = cat_state
    
    @classmethod
    def from_dict(cls, data: dict):
        pass

    def set_city_id(self, city_id: int):
        self.city_id = city_id

    def set_name(self, name: str):
        self.name = name
    
    def set_cat_state(self, cat_state: CatState):
        self.cat_state = cat_state

    def get_city_id(self):
        return copy.copy(self.city_id)

    def get_name(self):
        return copy.copy(self.name)
    
    def get_cat_state(self):
        return copy.copy(self.cat_state)
