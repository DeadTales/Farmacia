import copy

from Models.UserType import UserType
from Models.Address.Address import Address

class User:

    def __init__(self, nickname: str, first_name: str, 
                 last_name: str, pswd:str, user_type: UserType):
        self.nickname = nickname
        self.first_name = first_name
        self.last_name = last_name
        self.pswd = pswd
        self.user_type: UserType = user_type
     

    @classmethod
    def from_dict(cls, data: dict):
        if data:
            return cls(
                nickname = data.get("nickname"),
                first_name = data.get("firstname"),
                last_name = data.get("last_name"),
                pswd = data.get("pswd"),
                user_type = data.get("user_type")
            )

    
    def set_nickname(self, nickname: str):
        self.nickname = nickname
    
    def set_first_name(self, first_name: str):
        self.first_name = first_name

    def set_last_name(self, last_name: str):
        self.last_name = last_name
    
    def set_pswd(self, pswd: str):
        self.pswd = pswd
    
    def set_type_id(self, type_id: int):
        self.type_id = type_id

    def get_nickname(self):
        return copy.copy(self.nickname)

    def get_first_name(self):
        return copy.copy(self.first_name)

    def get_last_name(self):
        return copy.copy(self.last_name)

    def get_pswd(self):
        return copy.copy(self.pswd)

    def get_type_id(self):
        return copy.copy(self.type_id)