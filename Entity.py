#todo class entity
#adicionar um movable nas entities caso queiramos outros elementos moveis alem dos agentes
# coord em entity para termos as coords de todas as entidades

# Entity.py

class Entity:
    def __init__(self, coord):
        self.coord = coord
        self.movable = False

    def getCoord(self):
        return self.coord

    def isMovable(self):
        return self.movable
