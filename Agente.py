


# Class Agent
# __init__(name: String, freePositions: List of Coord) -> Void
# Attributes:
#     name : String
#     coord : Coord
#     finished_flag : Boolean
# Methods:
#  Raul :(  move(Coord) : Void
#   :)  finished() : Void
#   :(  nextMove(freePositions): Void
#  David :(  getLightHouseDirection : Vector



from random import random


class Agent:
    def __init__(self, name, freePositions):
        self.name = name
        self.finished_flag = False
        self.coord = freePositions.pop(random.randint(0, len(freePositions)-1))

    
    def move(self, coord):
        ##Por fazer
        return

    def finished(self):
        self.finished_flag = True

    def nextMove(self, freePositions):
        # Placeholder for movement logic
        if freePositions:
            self.move(freePositions[0])  # Move to the first free position

    def getLightHouseDirection(self, lighthouse):
        direction_x = lighthouse.x - self.x
        direction_y = lighthouse.y - self.y
        return (direction_x, direction_y)