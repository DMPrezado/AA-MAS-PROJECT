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

        self.ambient.agents.append(self)
        self.ambient.occupiedPositions.add(self.coord.as_tuple())

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

        agent_x, agent_y = self.coord.x, self.coord.y
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
        # definir ações banidas: não permitir PICK se não houver recurso aqui; não permitir DROP se não estiver no ninho ou não tiver recurso
        banned = set()
        if not self.ambient.has_resource_at(self.coord):
            banned.add(PICK_ACTION)
        here = self.ambient.getObject(self.coord)
        if not (self.has_resource and isinstance(here, Nest)):
            # se não estamos no ninho com recurso, banir DROP
            banned.add(DROP_ACTION)

        action = choose_action(
            state,
            actions=list(FORAGING_ACTIONS.keys()),
            banned_actions=banned,
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

        # update Q (apenas se estivermos em Q-learning)
        if Conf.MOVE_WITH_QLEARNING and self.last_state is not None and self.last_action is not None:
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

    def fixedPolicyChoice(self):
        """
        Política fixa (greedy/manhattan):
        1) Se estiver em cima de recurso e não tiver -> PICK
        2) Se estiver no ninho e tiver -> DROP
        3) Caso contrário:
            - se não tiver recurso: vai para o recurso mais próximo (greedy por Manhattan)
            - se tiver recurso: vai para o ninho
            - evita Wall/Limit/Fireplace
        """

        # 1) PICK se estou em cima do recurso
        if (not self.has_resource) and self.ambient.has_resource_at(self.coord):
            return PICK_ACTION

        # 2) DROP se estou no ninho
        here = self.ambient.getObject(self.coord)
        if self.has_resource and isinstance(here, Nest):
            return DROP_ACTION

        # 3) Escolher alvo
        if self.has_resource:
            tx, ty = self.ambient.getNest().getCoord().x, self.ambient.getNest().getCoord().y
        else:
            # recurso mais próximo
            if not self.ambient.resources:
                # se já não há recursos, vagueia
                return random.choice([0, 1, 2, 3])

            ax, ay = self.coord.x, self.coord.y
            best = None
            best_d = 10**9
            for r in self.ambient.resources:
                rx, ry = r.getCoord().x, r.getCoord().y
                d = abs(rx - ax) + abs(ry - ay)
                if d < best_d:
                    best_d = d
                    best = (rx, ry)

            tx, ty = best

        # direções possíveis (ação -> (dx,dy))
        directions = {
            0: (0, -1),  # up
            1: (0,  1),  # down
            2: (-1, 0),  # left
            3: (1,  0),  # right
        }

        def is_blocked(coord):
            obj = self.ambient.getObject(coord)
            if obj is None:
                return False
            if getattr(obj, "type", None) == "Limit":
                return True
            if isinstance(obj, Obstacle):
                # evita paredes e fogueiras
                t = obj.getType()
                return t in ("Wall", "Fireplace", "Limit")
            return False

        # 4) Greedy: escolhe o move que minimiza distância Manhattan ao alvo
        best_actions = []
        best_dist = 10**9

        for a, (dx, dy) in directions.items():
            nc = Coord.Coord(self.coord.x + dx, self.coord.y + dy)

            if is_blocked(nc):
                continue

            d = abs(tx - nc.x) + abs(ty - nc.y)
            if d < best_dist:
                best_dist = d
                best_actions = [a]
            elif d == best_dist:
                best_actions.append(a)

        # Se há boas escolhas, escolhe uma (com algum random para fugir a empates)
        if best_actions:
            return random.choice(best_actions)

        # 5) fallback: se tudo está bloqueado, tenta qualquer direção não bloqueada
        fallback = [a for a,(dx,dy) in directions.items()
                    if not is_blocked(Coord.Coord(self.coord.x + dx, self.coord.y + dy))]
        if fallback:
            return random.choice(fallback)

        # 6) se estiver encurralado total, não mexe (mas como só temos 0..5, devolve um move)
        return random.choice([0, 1, 2, 3])


    def executar(self):
        if Conf.NUMBER_RESOURCES == self.ambient.picked_resources:
            self.finished_flag = True
            return
        if Conf.MOVE_WITH_QLEARNING:
            action = self.movementChoice()
        elif Conf.MOVE_WITH_FIXED_POLICIES:
            action = self.fixedPolicyChoice()
            # para o fixed também faz sentido guardar isto (assim apply_action pode atualizar Q se quiseres)
            # nota: não guardamos last_state/last_action quando estamos em fixed — update_Q está condicionado a Conf.MOVE_WITH_QLEARNING
        else:
            raise ValueError("Config inválida em ConfForaging.py")

        self.apply_action(action)

