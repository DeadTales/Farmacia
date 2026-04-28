import copy

from Models.UserType import UserType
from Models.Address.Address import Address

class User:

    def __init__(self, user_id: int, first_name: str, 
                 last_name: str, user_type: UserType,
                 address: Address = None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_type: UserType = user_type
        self.address = address


    @classmethod
    def from_dict(cls, data: dict):
        pass
    
    def set_user_id(self, user_id: int):
        self.user_id = user_id
    
    def set_first_name(self, first_name: str):
        self.first_name = first_name

    def set_last_name(self, last_name: str):
        self.last_name = last_name
    
    def set_type_id(self, type_id: int):
        self.type_id = type_id

    def set_address(self, address: Address):
        self.address = address
    
    def get_user_id(self):
        return copy.copy(self.user_id)

    def get_first_name(self):
        return copy.copy(self.first_name)

    def get_last_name(self):
        return copy.copy(self.last_name)

    def get_type_id(self):
        return copy.copy(self.type_id)
    
    def get_address(self):
        return copy.copy(self.address)