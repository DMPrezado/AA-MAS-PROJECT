
# Coord.py

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, other):
        return isinstance(other, Coord) and self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"

    def as_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        """Coord + (dx,dy) ou Coord + Coord."""
        if isinstance(other, Coord):
            return Coord(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple) and len(other) == 2:
            dx, dy = other
            return Coord(self.x + dx, self.y + dy)
        raise TypeError("Coord só pode somar com Coord ou (dx,dy)")
    
    def __hash__(self):
        return hash((self.x, self.y))
