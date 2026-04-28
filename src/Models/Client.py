import copy

class Client:

    def __int__(self, email: str, first_name: str,
                last_name:str, rfc:str, phone:str,
                points: int):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.points = points

    @classmethod
    def from_dict(cls, data: dict):
        pass

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
    
    def get_email(self):
        return copy.copy(self.email)
    
    def get_first_name(self):
        return copy.copy(self.first_name)
    
    def get_lsat_name(self):
        return copy.copy(self.last_name)
    
    def get_phone(self):
        return copy.copy(self.phone)
    
    def get_points(self):
        return copy.copy(self.points)
    
    
    