import copy

from Models.Address.CatCity import CatCity

class CatSettlement:

    def __init__(self, settlement_id: int = None, name: str = None, 
                 cat_city: CatCity = None):
        self.settlement_id = settlement_id
        self.name = name
        self.cat_city = cat_city

    @classmethod
    def from_dict(cls, data: dict):
        if data:
            return cls(
                settlement_id = data.get("settlement_id"),
                name = data.get("name"),
                cat_city = CatCity.from_dict(data.get("cat_city")) if isinstance(data.get("cat_city"), dict) else data.get("cat_city")
            )
        

    def to_dict(self):
        return {
            "settlement_id": self.settlement_id,
            "name": self.name,
            "city_id": self.cat_city.get_city_id() if self.cat_city else None
        }

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
