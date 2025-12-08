
# Class Agent
# __init__(name: String, freePositions: List of Coord) -> Void
# Attributes:
#       name : String
#       coord : Coord
#       freePositions : List of Coord
#       finished_flag : Boolean
#       whereIsFront : Vector
#       ambient : Ambient
#       fitness : Int

# Methods:
#               executar() : Void   
    #               sensorFront() : (int, Object)
    #               sensorBack() : (int, Object)
    #               sensorLeft() : (int, Object)
    #               sensorRight() : (int, Object)
    #               sensorDirection() : (int, Object)
    #               movementChoice() : Coord ##vai para o algoritmo de aprendizagem e obtem um movimento
#                   moveTo(Coord) : Void    ##recebe uma reward pelo movimento executado


import pygad
import random

class Agent:
    def __init__(self, name, ambient):
        self.name = name
        self.finished_flag = False
        self.ambient = ambient
        freePositions = self.ambient.freePositions()
        self.coord = freePositions[random.randint(0, len(freePositions)-1)]
        self.ambient.occupiedPositions.add(self.coord)

    def executar(self):
        sensorDataFront = self.sensorFront()


    def sensorFront(self):
        