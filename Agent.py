import Entities
from MapImporter.Registry import register
import math
import Configuration as Conf

from qlearning import ACTIONS, choose_action, update_Q


MOVEMENTS={
        "FRONT" : (0 ,-1),
        "BACK"  : (0 , 1),
        "LEFT"  : (-1, 0),
        "RIGHT" : (1 , 0)
        }

@register("A")
class Agent:
    def __init__(self, coord, ambient=None):
        self.coord = coord
        self.ambient = ambient
        self.finished_flag = False
        self.fitness = 0
    
    def set_ambient(self, ambient):
        self.ambient = ambient
    
    
    # -----------------------------
    # Sensors
    # -----------------------------

    def _sense_in_direction(self, direction):
        steps = 0
        current = self.coord

        while True:
            current = current + MOVEMENTS.key(direction)
            obj = self.ambient.getObject(current)

            if obj is None:
                steps += 1
                continue

            obj_type = type(obj)

            return (steps, obj_type)
    
    def sensorDirection(self):
        ax, ay = self.coord.x, self.coord.y
        lh = self.ambient.getLightHouse().getCoord()
        lx, ly = lh.x, lh.y

        angle = math.degrees(math.atan2(ly - ay, lx - ax)) + 90
        angle = (angle + 180) % 360 - 180
        return angle


    # -----------------------------
    # EXECUTAR
    # -----------------------------
    def executar(self):
        if Conf.MOVE_WITH_QLEARNING:
            moveCoord = self.movementChoice()

        elif Conf.MOVE_WITH_FIXED_POLICIES:
            moveCoord = self.fixedPolicyChoice()

        else:
            raise ValueError(
            "Config inválida: escolhe 'fixed' ou 'qlearning' no Conf.py"
        )

        self.moveTo(moveCoord)
        
    def moveTo(self, newCoord):
        old_dist = self.distance_to_lighthouse()
        obj = self.ambient.getObject(newCoord)
        reward = 0

        # fora do mapa -> tratei como parede (se no vosso enunciado houver valor próprio, mete aqui)
        if obj is not None and obj.isObstacle:
            reward = obj.reward

        else:
            # livre ou farol
            self.ambient.occupiedPositions.discard(self.coord.as_tuple())
            self.coord = newCoord
            self.ambient.occupiedPositions.add(self.coord.as_tuple())

            lh = self.ambient.getLightHouse().getCoord()
            if self.coord.as_tuple() == lh.as_tuple():
                reward = obj.reward
                self.finished_flag = True
            else:
                new_dist = self.distance_to_lighthouse()
                if new_dist < old_dist:
                    reward = obj.REWARD_STEP_CLOSER
                else:
                    reward = obj.REWARD_STEP_AWAY

        self.fitness += reward

        if self.last_state is not None and self.last_action is not None:
            next_state = self.get_state()
            update_Q(self.last_state, self.last_action, reward, next_state)



    
    