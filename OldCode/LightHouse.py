# LightHouse
#     Attributes:
#         - coord: Coord
#     Methods:
#         - getCoord() -> Coord


# LightHouse.py

from Entity import Entity

class LightHouse(Entity):
    def __init__(self, coord):
        super().__init__(coord)
        self.type = "LightHouse"

