


# Class Agent
# __init__(name: String, freePositions: List of Coord) -> Void
# Attributes:
#     name : String
#     coord : Coord
#     finished_flag : Boolean
# Methods:
#  Raul     :(  move(Coord) : Void
#           :)  finished() : Void
#  David    :(  nextMove(freePositions): Void  (Já não vai haver freePositions como argumento)
#  David    :(  getLightHouseDirection : Vector



from random import random


class Agent:
    def __init__(self, name, ambient):
        self.name = name
        self.finished_flag = False
        self.ambient = ambient
        freePositions = self.ambient.freePositions()
        self.coord = freePositions[random.randint(0, len(freePositions)-1)]
        self.ambient.occupiedPositions.add(self.coord)
    
    def move(self, coord):
        ##Por fazer
        return

    def finished(self):
        self.finished_flag = True

    def nextMove(self, freePositions):
        # Placeholder for movement logic
        return #placeholder

    def getLightHouseDirection(self, lighthouse):
        direction_x = lighthouse.x - self.x
        direction_y = lighthouse.y - self.y
        return (direction_x, direction_y)