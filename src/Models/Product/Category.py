import copy

class Category:

    def __init__(self, category_id: int = None, name: str = None):
        self.category_id = category_id
        self.name = name

    
    @classmethod
    def from_dict(cls, data: dict):
        if data:
            return cls(
                category_id = data.get("category_id"),
                name = data.get("name")
            )

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name
        }
        

    def set_category_id(self, category_id: int):
        self.category_id = category_id

    def set_name(self, name:str):
        self.name = name

    def get_category_id(self):
        return copy.copy(self.category_id)

    def get_name(self):
        return copy.copy(self.name)
    
     
        
