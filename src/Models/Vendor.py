import copy

class Vendor:
    def __init__(self, vendor_id:str = None, name:str = None,
                 phone:str = None, email:str = None):
        self.vendor_id = vendor_id
        self.name = name
        self.phone = phone
        self.email = email

    @classmethod
    def from_dict(cls, data: dict):
        pass

    def set_vendor_id(self, vendor_id:str):
        self.vendor_id = vendor_id

    def set_name(self, name:str):
        self.name = name
    
    def set_phone(self, phone:str):
        self.phone = phone
    
    def set_email(self, email:str):
        self.email = email

    def get_vendor_id(self):
        return self.vendor_id
    
    def get_name(self):
        return self.name
    
    def get_phone(self):
        return self.phone
    
    def get_email(self):
        return self.email
    
    

