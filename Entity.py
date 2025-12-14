# Entity.py

class Entity:
    def __init__(self, coord):
        self.coord = coord
        self.movable = False
        self.type = "Entity"

    def getCoord(self):
        return self.coord

    def isMovable(self):
        return self.movable
