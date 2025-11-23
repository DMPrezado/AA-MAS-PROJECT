# Obstacle
#     Attributes:
#         - coord: Coord
#     Methods:
#         - getCoord() -> Coord

class Obstacle:
    def __init__(self, coord):
        self.coord = coord

    def getCoord(self):
        return self.coord