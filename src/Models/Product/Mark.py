import copy

from Models.Vendor import Vendor

class Mark:

    def __init__(self, mark_id: int = None, name: str = None, vendor: Vendor = None):
        self.mark_id = mark_id
        self.name = name
        self.vendor = Vendor
        