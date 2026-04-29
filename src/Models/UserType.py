import copy

class UserType:
    def __init__(self, type_id: int, name: str):
        self.type_id = type_id
        self.name = name

    @classmethod
    def from_dict(cls, data: dict):
        if data:
            return cls(
                type_id = data.get("type_id"),
                name = data.get("name")
            )


    def set_type_id(self, type_id: int):
        self.type_id = type_id

    def set_type_name(self, type_name: str):
        self.type_name = type_name

    def get_type_id(self):
        return copy.copy(self.type_id)
    
    def get_type_name(self):
        return copy.copy(self.type_name)
    
