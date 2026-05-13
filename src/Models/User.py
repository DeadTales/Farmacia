import copy

from Models.UserType import UserType
class User:

    def __init__(self, nickname: str = None, first_name: str = None, 
                 last_name: str = None, pswd:str = None, user_type: UserType = None):
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
                first_name = data.get("first_name"),
                last_name = data.get("last_name"),
                pswd = data.get("pswd"),
                user_type = UserType.from_dict(data.get("user_type")) if isinstance(data.get("user_type"), dict) else data.get("user_type")
            )
        
    def to_dict(self):
        return {
            "nickname": self.nickname,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pswd": self.pswd,
            "user_type": self.user_type.to_dict() if hasattr(self.user_type, "to_dict") else self.user_type,
        }     
            
    def set_nickname(self, nickname: str):
        self.nickname = nickname
    
    def set_first_name(self, first_name: str):
        self.first_name = first_name

    def set_last_name(self, last_name: str):
        self.last_name = last_name
    
    def set_pswd(self, pswd: str):
        self.pswd = pswd
    
    def set_type_id(self, type_id: int):
        if self.user_type:
            self.user_type.set_type_id(type_id)
        else:
            self.user_type = UserType(type_id=type_id, name=None)

    def get_nickname(self):
        return copy.copy(self.nickname)

    def get_first_name(self):
        return copy.copy(self.first_name)

    def get_last_name(self):
        return copy.copy(self.last_name)

    def get_pswd(self):
        return copy.copy(self.pswd)

    def get_type_id(self):
        return self.user_type.get_type_id() if self.user_type else None

    def get_user_type(self):
        return copy.copy(self.user_type)
