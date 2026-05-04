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
<<<<<<< HEAD
        return cls(
            vendor_id = data.get("vendor_id"),
            name = data.get("name"),
            phone = data.get("phone"),
            email = data.get("email")
        )
        
=======
        if data:
            return cls(
                vendor_id=data.get("vendor_id"),
                name=data.get("name"),
                phone=data.get("phone"),
                email=data.get("email")
            )

>>>>>>> 3139f9b920c2f2bfa81d7a016998ffea739531cd
    def to_dict(self):
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }
<<<<<<< HEAD
=======
        
>>>>>>> 3139f9b920c2f2bfa81d7a016998ffea739531cd

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
    
    

