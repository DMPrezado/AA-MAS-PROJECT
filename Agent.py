
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
import Coord
from Entity import Entity
from LightHouse import LightHouse
from Obstacle import Obstacle
from qlearning import ACTIONS, choose_action, update_Q


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
        return math.degrees(math.atan2(ly - ay, lx - ax))

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

        lh = self.ambient.getLightHouse().getCoord()
        dx = lh.x - self.coord.x
        dy = lh.y - self.coord.y

        def sign(v):
            if v > 0: return 1
            if v < 0: return -1
            return 0

        sx, sy = sign(dx), sign(dy)

        return (
            code.get(f_type, 6), bucket(f_dist),
            code.get(b_type, 6), bucket(b_dist),
            code.get(l_type, 6), bucket(l_dist),
            code.get(r_type, 6), bucket(r_dist),
            sx, sy
        )

    def distance_to_lighthouse(self):
        ax, ay = self.coord.x, self.coord.y
        lh = self.ambient.getLightHouse().getCoord()
        lx, ly = lh.x, lh.y
        return math.sqrt((lx - ax) ** 2 + (ly - ay) ** 2)

    # ---------- decisão (aprendizagem) ----------
    def movementChoice(self, sensorDataFront, sensorDataBack, sensorDataLeft, sensorDataRight, sensorDataDirection):
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
                reward = -30
            elif t == "Fireplace":
                # “caiu” -> entra e penaliza
                self.ambient.occupiedPositions.discard(self.coord.as_tuple())
                self.coord = newCoord
                self.ambient.occupiedPositions.add(self.coord.as_tuple())
                reward = -50
            else:
                reward = -30

        else:
            # livre ou farol
            self.ambient.occupiedPositions.discard(self.coord.as_tuple())
            self.coord = newCoord
            self.ambient.occupiedPositions.add(self.coord.as_tuple())

            lh = self.ambient.getLightHouse().getCoord()
            if self.coord.as_tuple() == lh.as_tuple():
                reward = 100
                self.finished_flag = True
            else:
                new_dist = self.distance_to_lighthouse()
                reward = 10 if new_dist < old_dist else -15

        self.fitness += reward

        if self.last_state is not None and self.last_action is not None:
            next_state = self.get_state()
            update_Q(self.last_state, self.last_action, reward, next_state)

    def executar(self):
        f = self.sensorFront()
        b = self.sensorBack()
        l = self.sensorLeft()
        r = self.sensorRight()
        d = self.sensorDirection()

        moveCoord = self.movementChoice(f, b, l, r, d)
        self.moveTo(moveCoord)


