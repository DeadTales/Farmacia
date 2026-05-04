import copy

from Models.Address.Address import Address

class Client:

    def __init__(self, email: str, first_name: str,
                last_name:str, rfc:str, phone:str,
                points: int, address: Address = None):
        
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.rfc = rfc
        self.phone = phone
        self.points = points
        self.address = address


    @classmethod
    def from_dict(cls, data: dict):
        if data:
            return cls(
                email=data.get("email"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                rfc=data.get("rfc"),
                phone=data.get("phone"),
                points=data.get("points"),
                address=data.get("address")  
            )

    def to_dict(self):
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "rfc": self.rfc,
            "phone": self.phone,
            "points": self.points,
            "address": self.address
        }

    def set_email(self, email:str):
        self.email = email
    
    def set_first_name(self, first_name: str):
        self.first_name = first_name
    
    def set_last_name(self, last_name: str):
        self.last_name = last_name
    
    def set_phone(self, phone: str):
        self.phone = phone
    
    def set_points(self, points: int):
        self.points = points
    
    def set_address(self, address: Address):
        self.address = address
    
    
    def get_email(self):
        return copy.copy(self.email)
    
    def get_first_name(self):
        return copy.copy(self.first_name)
    
    def get_last_name(self):
        return copy.copy(self.last_name)
    
    def get_phone(self):
        return copy.copy(self.phone)
    
    def get_points(self):
        return copy.copy(self.points)
    
    def get_address(self):
        return copy.copy(self.address)
    
