import math
import random
import Coord
from Entity import Entity
from Obstacle import Obstacle
from Nest import Nest
from Resource import Resource
from ConfForaging import ConfigForaging as Conf
from qlearning import choose_action, update_Q

# AÇÕES do Foraging
FORAGING_ACTIONS = {
    0: (0, -1),  # up
    1: (0,  1),  # down
    2: (-1, 0),  # left
    3: (1,  0),  # right
    4: None,     # PICK
    5: None,     # DROP
}

MOVE_ACTIONS = {0, 1, 2, 3}
PICK_ACTION = 4
DROP_ACTION = 5


class ForagingAgent(Entity):
    def __init__(self, name, ambient, pos):
        super().__init__(pos)
        self.type = "ForagingAgent"
        self.name = name
        self.ambient = ambient

        self.fitness = 0
        self.finished_flag = False

        self.whereIsFront = (0, -1)
        self.movable = True

        self.has_resource = False
        self.steps_since_pickup = 0
        self.steps_carrying = 0

        self.last_state = None
        self.last_action = None

        self.ambient.occupiedPositions.add(self.coord.as_tuple())

        self.on_resource=False
        self.on_nest=False



    def getX(self):
m        return self.coord.getX()
    
    def getY(self):
        return self.coord.getY()
    
    def getCoord(self):
        return self.coord

    # --------------------------
    # SENSORES
    # --------------------------

    def sensorNestVector(self):
        nest = self.ambient.getNest()
        if nest is None:
            return (0, 0)
        n = nest.getCoord()
        return (n.x - self.coord.x, n.y - self.coord.y)

    def sensorNearestResourceVector(self):
        """(dx, dy) para o recurso mais próximo (Manhattan). Se não houver, (0, 0)."""
        if not self.ambient.resources:
            return (0, 0)

        agent_x, agent_y = self.getX(), self.getY()
        closest_dx, closest_dy = 0, 0
        min_distance = float("inf")

        for resource in self.ambient.resources:
            resource_x = resource.getCoord().x
            resource_y = resource.getCoord().y

            distance = abs(resource_x - agent_x) + abs(resource_y - agent_y)

            if distance < min_distance:
                min_distance = distance
                closest_dx = resource_x - agent_x
                closest_dy = resource_y - agent_y

        return (closest_dx, closest_dy)


    def _coord_after_move(self, action):
        dx, dy = FORAGING_ACTIONS[action]
        return Coord.Coord(self.coord.x + dx, self.coord.y + dy)

    # --------------------------
    # ESTADO (compacto)
    # --------------------------

    def get_state(self):
        def sign(v):
            return -1 if v < 0 else (1 if v > 0 else 0)

        ndx, ndy = self.sensorNestVector()
        rdx, rdy = self.sensorNearestResourceVector()

        here = self.ambient.getObject(self.coord)
        on_resource = 1 if self.ambient.has_resource_at(self.coord) else 0
        on_nest = 1 if isinstance(here, Nest) else 0

        # bloqueios 4-dir (só contexto; não bloqueia ações)
        def blocked(dx, dy):
            c = Coord.Coord(self.coord.x + dx, self.coord.y + dy)
            obj = self.ambient.getObject(c)
            if obj is None:
                return 0
            if getattr(obj, "type", None) == "Limit":
                return 1
            if isinstance(obj, Obstacle):
                return 1
            return 0

        bn = blocked(0, -1)
        bs = blocked(0,  1)
        bw = blocked(-1, 0)
        be = blocked(1,  0)

        return (
            sign(ndx), sign(ndy),          # direção do ninho
            sign(rdx), sign(rdy),          # direção do recurso mais próximo
            1 if self.has_resource else 0, # a carregar?
            on_resource, on_nest,
            bn, bs, bw, be
        )

    # --------------------------
    # ESCOLHA (Q-learning) - SEM BLOQUEAR AÇÕES
    # --------------------------

    def movementChoice(self):
        state = self.get_state()
        action = choose_action(
            state,
            actions=list(FORAGING_ACTIONS.keys()),
            task="foraging"
        )
        self.last_state = state
        self.last_action = action
        return action

    # --------------------------
    # EXECUÇÃO + RECOMPENSAS + UPDATE Q
    # --------------------------

    def apply_action(self, action):
        reward = Conf.STEP_COST

        # ---------------- MOVE ----------------
        if action in MOVE_ACTIONS:
            # distância ao alvo ANTES do move (para shaping)
            if self.has_resource:
                ndx, ndy = self.sensorNestVector()
                old_d = abs(ndx) + abs(ndy)
            else:
                rdx, rdy = self.sensorNearestResourceVector()
                old_d = abs(rdx) + abs(rdy)

            newCoord = self._coord_after_move(action)
            obj = self.ambient.getObject(newCoord)

            dx, dy = FORAGING_ACTIONS[action]
            self.whereIsFront = (dx, dy)

            move_ok = False

            if obj is not None and getattr(obj, "type", None) == "Limit":
                reward += Conf.REWARD_HIT_WALL_OR_LIMIT

            elif isinstance(obj, Obstacle):
                t = obj.getType()
                if t == "Fireplace":
                    reward += Conf.REWARD_IN_FIREPLACE
                else:
                    reward += Conf.REWARD_HIT_WALL_OR_LIMIT

            else:
                # move válido
                self.ambient.occupiedPositions.discard(self.coord.as_tuple())
                self.coord = newCoord
                self.ambient.occupiedPositions.add(self.coord.as_tuple())
                move_ok = True

                # contadores
                if self.has_resource:
                    self.steps_carrying += 1
                else:
                    self.steps_since_pickup += 1

            # shaping se moveu com sucesso
            if move_ok:
                if self.has_resource:
                    ndx2, ndy2 = self.sensorNestVector()
                    new_d = abs(ndx2) + abs(ndy2)
                else:
                    rdx2, rdy2 = self.sensorNearestResourceVector()
                    new_d = abs(rdx2) + abs(rdy2)

                if new_d < old_d:
                    reward += Conf.REWARD_MOVE_CLOSER_TARGET
                elif new_d > old_d:
                    reward += Conf.REWARD_MOVE_AWAY_TARGET

        # ---------------- PICK ----------------
        elif action == PICK_ACTION:
            if (not self.has_resource) and self.ambient.has_resource_at(self.coord):
                ok = self.ambient.remove_resource_at(self.coord)
                if ok:
                    self.has_resource = True
                    self.steps_since_pickup = 0
                    self.steps_carrying = 0
                    reward += Conf.REWARD_PICK_RESOURCE
                else:
                    reward += Conf.REWARD_INVALID_PICK
            else:
                reward += Conf.REWARD_INVALID_PICK


        # ---------------- DROP ----------------
        elif action == DROP_ACTION:
            here = self.ambient.getObject(self.coord)
            if self.has_resource and isinstance(here, Nest):
                self.has_resource = False
                self.steps_carrying = 0
                reward += Conf.REWARD_DROP_IN_NEST
                self.ambient.picked_resources += 1
            else:
                reward += Conf.REWARD_INVALID_DROP

        # ---------------- penalizações a cada 5 passos ----------------
        if (not self.has_resource) and self.steps_since_pickup > 0 and self.steps_since_pickup % 5 == 0:
            reward += Conf.PENALTY_5_STEPS_NO_PICKUP

        if self.has_resource and self.steps_carrying > 0 and self.steps_carrying % 5 == 0:
            reward += Conf.PENALTY_5_STEPS_CARRYING

        # fitness
        self.fitness += reward

        # update Q
        if self.last_state is not None and self.last_action is not None:
            next_state = self.get_state()
            update_Q(
                self.last_state,
                self.last_action,
                reward,
                next_state,
                actions=list(FORAGING_ACTIONS.keys()),
                task="foraging"
            )

    # --------------------------
    # FIXED POLICY (opcional)
    # --------------------------

    def moveTo(self, newCoord):
        reward = 0

        self.coord = newCoord




    def fixedPolicyChoice(self):
        front = self.whereIsFront
        back  = (-front[0], -front[1])
        left  = (-front[1], front[0])
        right = (front[1], -front[0])

        def sensorDirection(tuple_coord):
            goal_x, goal_y = tuple_coord[0], tuple_coord[1]
            ax ,ay = self.coord.x, self.coord.y

            angle = math.degrees(math.atan2(goal_x - ay, goal_y - ax)) + 90
            angle = (angle + 180) % 360 - 180
            return angle

        def step(direction):
            dx, dy = direction
            return Coord.Coord(self.coord.x + dx, self.coord.y + dy)

        def is_free(c):
            obj = self.ambient.getObject(c)
            if isinstance(obj, Resource):
                return "R"
            if isinstance(obj, Nest):
                return "N"
            if obj is not None:
                return "O"

        def searchResouce():
            resourceCoord_asTuple = self.sensorNearestResourceVector()
            angle = sensorDirection(resourceCoord_asTuple)
            
            if random.random() < 0.45:
                directions = [front, left, right, back]
                random.shuffle(directions)
                for d in directions:
                    c = step(d)
                    if is_free(c) == "R":
                        self.on_resource=True
                        return self.coord + c
                    elif is_free(c) != "O": 
                        return self.coord + c

    
        # 3) Caso contrário, usa o ângulo
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
                    if is_free(c) == "R":
                        self.on_resource=True
                        return self.coord + c
                    elif is_free(c) != "O": 
                        return self.coord + c
                
        def searchNest():
            nestCoord_asTuple = self.sensorNestVector()
            angle = sensorDirection(nestCoord_asTuple)
            
            if random.random() < 0.45:
                directions = [front, left, right, back]
                random.shuffle(directions)
                for d in directions:
                    c = step(d)
                    if is_free(c) == "N":
                        self.on_nest=True
                        return self.coord + c
                    elif is_free(c) != "O": 
                        return self.coord + c

    
        # 3) Caso contrário, usa o ângulo
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
                if is_free(c) == "N":
                    self.on_nest=True
                    return self.coord + c
                elif is_free(c) != "O": 
                    return self.coord + c

        def pick():
            self.on_resource=False
            self.ambient.remove_resource_at(self.coord)
            self.has_resource = True
            return self.coord  # ação de PICK
        
        def drop():
            self.on_nest=False
            self.has_resource = False
            self.ambient.picked_resources += 1
            return self.coord  # ação de DROP

        carrying = self.has_resource

        if not carrying:
            self.moveTo(searchResouce())
        if not carrying and self.on_resource:
            pick()

        if carrying:
            self.moveTo(searchNest())
        if carrying and self.on_nest:
            drop()



    


    def executar(self):
        if Conf.NUMBER_RESOURCES == self.ambient.picked_resources:
            self.finished_flag = True
            return
        if Conf.MOVE_WITH_QLEARNING:
            action = self.movementChoice()
            self.apply_action(action)
        elif Conf.MOVE_WITH_FIXED_POLICIES:
            self.fixedPolicyChoice()
        else:
            raise ValueError("Config inválida em ConfForaging.py")




