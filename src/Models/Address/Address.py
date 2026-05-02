import copy
from Models.Address.CatSettlement import CatSettlement

class Address:
    
    def __init__(self, address_id: int = None, street: str = None, 
                 ext_num: str = None, inter_num: str = None, 
                 cat_settlement: CatSettlement = None):

        self.address_id = address_id
        self.street = street
        self.ext_num = ext_num
        self.inter_num = inter_num
        self.cat_settlement = cat_settlement

    
    @classmethod
    def from_dict(cls, data: dict):
        if data:
            return cls(
                address_id = data.get("addres_id"),
                street = data.get("street"),
                ext_num = data.get("external_number"),
                inter_num = data.get("internal_number"),
                cat_settlement = data.get("cat_settlement")
            )
    
    def to_dict(self):
        return {
            "address_id": self.address_id,
            "street": self.street,
            "external_number": self.ext_num,
            "internal_number": self.inter_num,
            "settlement_id": self.cat_settlement.get_settlement_id()
        }

    def set_address_id(self, address_id: int):
        self.address_id = address_id
    
    def set_street(self, street: str):
        self.street = street
    
    def set_ext_num(self, ext_num: str):
        self.ext_num = ext_num
    
    def set_inter_num(self, inter_num: str):
        self.inter_num = inter_num
    
    def set_settlement(self, cat_settlement: CatSettlement):
        self.cat_settlement = cat_settlement
    
    def get_address_id(self):
        return copy.copy(self.address_id)
    
    def get_street(self):
        return copy.copy(self.street)
    
    def get_ext_num(self):
        return copy.copy(self.ext_num)
    
    def get_inter_num(self):
        return copy.copy(self.inter_num)
    
    def get_settlement(self):
        return copy.copy(self.cat_settlement)
    
