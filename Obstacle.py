# Obstacle
#     Attributes:
#         - coord: Coord
#     Methods:
#         - getCoord() -> Coord


# Obstacle.py

from Entity import Entity

class Obstacle(Entity):
    def __init__(self, coord, obj_type="Wall"):
        super().__init__(coord)
        self.type = obj_type   # 'Wall', 'Fireplace', 'Limit', ...

    def getType(self):
        return self.type
