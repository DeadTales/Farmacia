import copy

from Models.Vendor import Vendor

class Mark:

    def __init__(self, mark_id: int = None, name: str = None, vendor: Vendor = None):
        self.mark_id = mark_id
        self.name = name
        self.vendor = Vendor
        
    @classmethod
    def from_dict(cls, data: dict):
        if (data):
            return cls(
                mark_id = data.get("mark_id"),
                name = data.get("name"),
                vendor = data.get("vendor")
            )

        return None
    
    def to_dict(self):
        return {
            "mark_id": self.mark_id,
            "name": self.name,
            "vendor_id": self.vendor.get_vendor_id()
        }