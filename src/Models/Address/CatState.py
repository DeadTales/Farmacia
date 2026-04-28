import copy

class CatState:
    def __init__(self, state_id: int = None, name: str = None):
        self.state_id = state_id
        self.name = name

    @classmethod
    def from_dict(cls, data: dict):
        pass

    def set_state_id(self, state_id: int):
        self.state_id = state_id

    def set_name(self, name:str):
        self.name = name

    def get_state_id(self):
        return copy.copy(self.state_id)
    
    def get_name(self):
        return copy.copy(self.name)
    