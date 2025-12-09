# LightHouse
#     Attributes:
#         - coord: Coord
#     Methods:
#         - getCoord() -> Coord
from Entity import Entity

class LightHouse(Entity):
    def __init__(self, coord):
        self.coord = coord

    def getCoord(self):
        return self.coord