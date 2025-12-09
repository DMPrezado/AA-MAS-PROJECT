# Obstacle
#     Attributes:
#         - coord: Coord
#     Methods:
#         - getCoord() -> Coord
from Entity import Entity
class Obstacle(Entity):
    def __init__(self, coord):
        self.coord = coord

#    def getCoord(self):
#       return self.coord