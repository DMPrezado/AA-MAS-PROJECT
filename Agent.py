
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


# Agent.py
import math
import random
import Coord
from Entity import Entity
from LightHouse import LightHouse
from Obstacle import Obstacle
from qlearning import ACTIONS, choose_action, update_Q
from Conf import ConfigLightHouse as Conf



class Agent(Entity):
    def __init__(self, name, ambient, pos):
        super().__init__(pos)
        self.type = "Agent"
        self.name = name
        self.ambient = ambient

        self.finished_flag = False
        self.fitness = 0

        self.whereIsFront = (0, -1)
        self.movable = True

        self.last_state = None
        self.last_action = None

        self.ambient.agents.append(self)
        self.ambient.occupiedPositions.add(self.coord.as_tuple())


    def getObject(self, coord):
        for o in self.ambient.obstacles:
            if o.getCoord().as_tuple() == coord.as_tuple():
                return o
        for a in self.ambient.agents:
            if a.getCoord().as_tuple() == coord.as_tuple():
                return a
        for lh in [self.ambient.lighthouse]:
            if lh.getCoord().as_tuple() == coord.as_tuple():
                return lh
        return None

    # ---------- sensores ----------
    def _sense_in_direction(self, direction):
        dx, dy = direction
        steps = 0
        current = self.coord

        while True:
            current = current + (dx, dy)
            obj = self.ambient.getObject(current)

            if obj is None:
                steps += 1
                continue

            obj_type = getattr(obj, "type", None)

            if isinstance(obj, LightHouse):
                obj_type = "LightHouse"
            elif isinstance(obj, Obstacle):
                obj_type = obj.getType()
            elif hasattr(obj, "movable") and obj.movable:
                obj_type = "Agent"
            elif obj_type is None:
                obj_type = "Other"

            return (steps, obj_type)

    def sensorFront(self):
        return self._sense_in_direction(self.whereIsFront)

    def sensorBack(self):
        fx, fy = self.whereIsFront
        return self._sense_in_direction((-fx, -fy))

    def sensorLeft(self):
        fx, fy = self.whereIsFront
        return self._sense_in_direction((-fy, fx))

    def sensorRight(self):
        fx, fy = self.whereIsFront
        return self._sense_in_direction((fy, -fx))

    def sensorDirection(self):
        ax, ay = self.coord.x, self.coord.y
        lh = self.ambient.getLightHouse().getCoord()
        lx, ly = lh.x, lh.y

        angle = math.degrees(math.atan2(ly - ay, lx - ax)) + 90
        angle = (angle + 180) % 360 - 180
        return angle


    # ---------- estado ----------
    def get_state(self):
        code = {
            None: 0,
            "LightHouse": 1,
            "Wall": 2,
            "Fireplace": 3,
            "Limit": 4,
            "Border": 4,
            "Agent": 5,
            "Other": 6,
        }

        def bucket(d):
            if d == 0: return 0
            if d == 1: return 1
            if d <= 3: return 2
            return 3

        f_dist, f_type = self.sensorFront()
        b_dist, b_type = self.sensorBack()
        l_dist, l_type = self.sensorLeft()
        r_dist, r_type = self.sensorRight()
        lh_angle       = self.sensorDirection()


        return (
            code.get(f_type, 6), bucket(f_dist),
            code.get(b_type, 6), bucket(b_dist),
            code.get(l_type, 6), bucket(l_dist),
            code.get(r_type, 6), bucket(r_dist),
            lh_angle
        )

    def distance_to_lighthouse(self):
        ax, ay = self.coord.x, self.coord.y
        lh = self.ambient.getLightHouse().getCoord()
        lx, ly = lh.x, lh.y
        return math.sqrt((lx - ax) ** 2 + (ly - ay) ** 2)

    # ---------- decisão (aprendizagem) ----------
    def movementChoice(self):
        state = self.get_state()
        action = choose_action(state)

        self.last_state = state
        self.last_action = action

        dx, dy = ACTIONS[action]
        return Coord.Coord(self.coord.x + dx, self.coord.y + dy)

    # ---------- execução + recompensa + update Q ----------
    def moveTo(self, newCoord):
        old_dist = self.distance_to_lighthouse()
        obj = self.ambient.getObject(newCoord)
        reward = 0

        # fora do mapa -> tratei como parede (se no vosso enunciado houver valor próprio, mete aqui)
        if obj is not None and getattr(obj, "type", None) == "Limit":
            reward = -30

        elif isinstance(obj, Obstacle):
            t = obj.getType()
            if t == "Wall":
                reward = Conf.REWARD_HIT_WALL

            elif t == "Fireplace":
                reward = Conf.REWARD_IN_FIREPLACE

            else:
                reward = Conf.REWARD_HIT_OBJECT

        else:
            # livre ou farol
            self.ambient.occupiedPositions.discard(self.coord.as_tuple())
            self.coord = newCoord
            self.ambient.occupiedPositions.add(self.coord.as_tuple())

            lh = self.ambient.getLightHouse().getCoord()
            if self.coord.as_tuple() == lh.as_tuple():
                reward = Conf.REWARD_REACH_GOAL
                self.finished_flag = True
            else:
                new_dist = self.distance_to_lighthouse()
                if new_dist < old_dist:
                    reward = Conf.REWARD_STEP_CLOSER
                else:
                    reward = Conf.REWARD_STEP_AWAY

        self.fitness += reward

        if self.last_state is not None and self.last_action is not None:
            next_state = self.get_state()
            update_Q(self.last_state, self.last_action, reward, next_state)




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




    def fixedPolicyChoice(self):
        f_dist, f_type = self.sensorFront()
        b_dist, b_type = self.sensorBack()
        l_dist, l_type = self.sensorLeft()
        r_dist, r_type = self.sensorRight()
        angle = self.sensorDirection()

        front = self.whereIsFront
        back  = (-front[0], -front[1])
        left  = (-front[1], front[0])
        right = (front[1], -front[0])

        def step(direction):
            dx, dy = direction
            return Coord.Coord(self.coord.x + dx, self.coord.y + dy)

        def is_free(c):
            obj = self.ambient.getObject(c)
            return (obj is None) or isinstance(obj, LightHouse)

    # 1) Se o farol estiver visível, ir direto
        if f_type == "LightHouse" and f_dist > 0:
            c = step(front)
            return c if is_free(c) else self.coord

        if l_type == "LightHouse" and l_dist > 0:
            c = step(left)
            return c if is_free(c) else self.coord

        if r_type == "LightHouse" and r_dist > 0:
            c = step(right)
            return c if is_free(c) else self.coord

        if b_type == "LightHouse" and b_dist > 0:
            c = step(back)
            return c if is_free(c) else self.coord

    # 2) Caso contrário, usa o ângulo
        if -45 <= angle <= 45:
            preferred = [front, left, right, back]
        elif 45 < angle <= 135:
            preferred = [left, front, back, right]
        elif -135 <= angle < -45:
            preferred = [right, front, back, left]
        else:
            preferred = [back, left, right, front]

        for d in preferred:
            c = step(d)
            if is_free(c):
                return c

    # 3) Fica parado se não houver alternativa
        return self.coord

            


