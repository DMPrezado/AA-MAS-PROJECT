# Resource.py
from Entity import Entity

class Resource(Entity):
    def __init__(self, coord, value=1):
        super().__init__(coord)
        self.type = "Resource"
        self.value = value
