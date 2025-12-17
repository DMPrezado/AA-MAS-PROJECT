# Nest.py
from Entity import Entity

class Nest(Entity):
    def __init__(self, coord):
        super().__init__(coord)
        self.type = "Nest"
