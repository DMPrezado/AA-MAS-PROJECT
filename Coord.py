# Coord
#     Attributes:
#         - x: int
#         - y: int
#     Methods:
#         - getX() -> int
#         - getY() -> int
#         - setX(x: int) -> Coord (returns new Coord)
#         - setY(y: int) -> Coord (returns new Coord)
#         - __eq__(other) -> bool
#         - __repr__() / __str__() -> str
#         - distance_to(other: Coord) -> float
#         - as_tuple() -> tuple[int,int]

# Coord.py

class Coord(tuple):
    """
    Immutable, hashable coordinate represented as a tuple (x, y).
    Backwards-compatible API with previous Coord class: attributes x,y and
    methods getX/getY/setX/setY/as_tuple and __add__.
    """
    def __new__(cls, x, y):
        return super().__new__(cls, (int(x), int(y)))

    # keep __init__ empty because tuple is already initialised in __new__
    def __init__(self, x, y):
        pass

    @property
    def x(self):
        return int(self[0])

    @property
    def y(self):
        return int(self[1])

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        return Coord(int(x), self.y)

    def setY(self, y):
        return Coord(self.x, int(y))

    def __eq__(self, other):
        if isinstance(other, Coord):
            return tuple.__eq__(self, other)
        if isinstance(other, tuple):
            return tuple.__eq__(self, other)
        return False

    def __hash__(self):
        return tuple.__hash__(self)

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"

    def as_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        """Support Coord + Coord or Coord + (dx,dy) and return Coord."""
        if isinstance(other, Coord) or isinstance(other, tuple):
            if len(other) != 2:
                raise TypeError("Coord só pode somar com Coord ou (dx,dy)")
            dx, dy = other[0], other[1]
            return Coord(self.x + int(dx), self.y + int(dy))
        raise TypeError("Coord só pode somar com Coord ou (dx,dy)")


# Utility conversion functions (backwards compatibility and centralised conversions)

def coord_to_tuple(coord):
    """Converte Coord.Coord ou tuple para um tuple (int,int).
    Aceita também objectos com atributos .x/.y.
    """
    # Coord has as_tuple and properties x/y
    if isinstance(coord, Coord):
        return coord.as_tuple()
    if isinstance(coord, tuple):
        if len(coord) != 2:
            raise TypeError("Tuplo de coordenadas deve ter comprimento 2")
        return (int(coord[0]), int(coord[1]))
    if hasattr(coord, "x") and hasattr(coord, "y"):
        return (int(coord.x), int(coord.y))
    raise TypeError("coord deve ser Coord ou (x,y)")


def coord_to_coord(coord):
    """Converte tuple ou Coord.Coord para um Coord.Coord object.
    """
    if isinstance(coord, Coord):
        return coord
    if isinstance(coord, tuple):
        if len(coord) != 2:
            raise TypeError("Tuplo de coordenadas deve ter comprimento 2")
        return Coord(int(coord[0]), int(coord[1]))
    if hasattr(coord, "x") and hasattr(coord, "y"):
        return Coord(int(coord.x), int(coord.y))
    raise TypeError("coord deve ser Coord ou (x,y)")
