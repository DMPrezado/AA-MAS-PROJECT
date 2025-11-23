# Coord
#     Attributes:
#         - x: int
#         - y: int
#     Methods:
#         - getX() -> int
#         - getY() -> int
#         - setX(x: int) -> None
#         - setY(y: int) -> None
#         - __eq__(other) -> bool
#         - __repr__() / __str__() -> str
#         - distance_to(other: Coord) -> float
#         - as_tuple() -> tuple[int,int]

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coord):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"

    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def as_tuple(self):
        return (self.x, self.y)