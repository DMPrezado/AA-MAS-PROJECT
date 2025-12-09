
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


import math
import pygad
import random
import Coord

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
        sensorDataBack = self.sensorBack()
        sensorDataLeft = self.sensorLeft()
        sensorDataRight = self.sensorRight()
        sensorDataDirection = self.sensorDirection()
        moveCoord = self.movementChoice(sensorDataFront, sensorDataBack, sensorDataLeft, sensorDataRight, sensorDataDirection)
        self.moveTo(moveCoord)



    def sensorFront(self):
        result = (0, None)
        direction = self.whereIsFront
        while True:
            sensorCoord = self.coord + direction
            if sensorCoord in self.freePositions:
                result._1 += 1
            else:
                result._2 = self.ambient.getObject(sensorCoord).type
                break
        return result
        
    def sensorBack(self):
        result = (0, None)
        direction = (self.whereIsFront[0] * -1, self.whereIsFront[1] * -1)
        while True:
            sensorCoord = self.coord + direction
            if sensorCoord in self.freePositions:
                result._1 += 1
            else:
                result._2 = self.ambient.getObject(sensorCoord).type
                break
        return result
        
    def sensorLeft(self):
        result = (0, None)
        direction = (-self.whereIsFront[1], self.whereIsFront[0])
        while True:
            sensorCoord = self.coord + direction
            if sensorCoord in self.freePositions:
                result._1 += 1
            else:
                result._2 = self.ambient.getObject(sensorCoord).type
                break
        return result
    
    def sensorRight(self):
        result = (0, None)
        direction = (self.whereIsFront[1], -self.whereIsFront[0])
        while True:
            sensorCoord = self.coord + direction
            if sensorCoord in self.freePositions:
                result._1 += 1
            else:
                result._2 = self.ambient.getObject(sensorCoord).type
                break
        return result
    

    def sensorDirection(self):
        ax, ay = self.coord
        lx, ly = self.ambient.getLightHouse().getCoord()
        return math.degrees(math.atan2(ly - ay, lx - ax))

    def movementChoice(self, sensorDataFront, sensorDataBack, sensorDataLeft, sensorDataRight, sensorDataDirection):
        # Placeholder for movement choice logic using sensor data
        # This should interface with a learning algorithm to decide the next move
        #
        #
        #
        #


        possibleMoves = [
            Coord.Coord(self.coord.x + 1, self.coord.y),  # Move Right
            Coord.Coord(self.coord.x - 1, self.coord.y),  # Move Left
            Coord.Coord(self.coord.x, self.coord.y + 1),  # Move Down
            Coord.Coord(self.coord.x, self.coord.y - 1)   # Move Up
        ]
        # Filter possible moves to only include free positions
        freeMoves = [move for move in possibleMoves if move in self.ambient.freePositions()]
        if freeMoves:
            return random.choice(freeMoves)
        else:
            return self.coord  # No move possible, stay in place

    def moveTo(self, newCoord):
        oldCoord = self.coord
        if newCoord in self.ambient.freePositions():
            self.ambient.occupiedPositions.remove(self.coord.as_tuple())
            self.coord = newCoord
            self.ambient.occupiedPositions.add(self.coord.as_tuple())
            self.updateFitness(newCoord, oldCoord)
        else:
            obj = self.ambient.getObject(newCoord)
            obj_type = getattr(obj, "type", None)

            if obj_type == 'Wall':
                self.fitness -= 20
            elif obj_type == 'Fireplace':
                self.fitness -= 10
            elif obj_type in ('Limit', 'Border'):
                self.fitness -= 25
            # Penalize for invalid move
        
    def getLightHouseDistance(self):
        ax, ay = self.coord.x, self.coord.y
        lx, ly = self.ambient.getLightHouse().getCoord().x, self.ambient.getLightHouse().getCoord().y
        return math.sqrt((lx - ax) ** 2 + (ly - ay) ** 2)
    
    def updateFitness(self, newCoord, oldCoord):
        oldDistance = self.getLightHouseDistance(oldCoord)
        newDistance = self.getLightHouseDistance(newCoord)
        if newDistance < oldDistance:
            self.fitness += 10  # Reward for moving closer
        else:
            self.fitness -= 15  # Penalty for moving away