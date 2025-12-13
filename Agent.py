
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


class Agent(Entity):
    def __init__(self, name, ambient, pos):
        super().__init__(pos)
        self.name = name
        self.finished_flag = False
        self.ambient = ambient
        self.fitness = 0
        self.whereIsFront = (0, -1)  # a apontar para cima
        self.movable = True

        # para Q-learning
        self.last_state = None
        self.last_action = None

        # registar no ambiente
        self.ambient.agents.append(self)
        self.ambient.occupiedPositions.add(self.coord.as_tuple())

    # --------------------------
    # SENSORES – FUNÇÃO AUXILIAR
    # --------------------------
    def _sense_in_direction(self, direction):
        """
        Dispara um “raio” na direção (dx, dy).
        Conta células livres até bater em algo.
        Devolve (distancia_livre: int, tipo_objeto: str ou None).
        """
        dx, dy = direction
        steps = 0
        current = self.coord

        while True:
            current = current + (dx, dy)
            obj = self.ambient.getObject(current)

            if obj is None:
                steps += 1
                continue

            # apanhou alguma coisa
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

    # --------------------------
    # SENSORES PÚBLICOS
    # --------------------------
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
        """
        Ângulo (graus) para o farol.
        """
        ax, ay = self.coord.x, self.coord.y
        lh = self.ambient.getLightHouse().getCoord()
        lx, ly = lh.x, lh.y
        return math.degrees(math.atan2(ly - ay, lx - ax))

    # --------------------------
    # ESTADO PARA Q-LEARNING
    # --------------------------
    def get_state(self):
        """
        Estado = (front_type, back_type, left_type, right_type, sx, sy)
        codificando tipo por números simples.
        """
        # mapear tipo para código inteiro
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

        f_dist, f_type = self.sensorFront()
        b_dist, b_type = self.sensorBack()
        l_dist, l_type = self.sensorLeft()
        r_dist, r_type = self.sensorRight()

        f_code = code.get(f_type, 6)
        b_code = code.get(b_type, 6)
        l_code = code.get(l_type, 6)
        r_code = code.get(r_type, 6)

        # direção grossa para o farol
        lh = self.ambient.getLightHouse().getCoord()
        dx = lh.x - self.coord.x
        dy = lh.y - self.coord.y

        def sign(v):
            if v > 0: return 1
            if v < 0: return -1
            return 0

        sx = sign(dx)
        sy = sign(dy)

        return (f_code, b_code, l_code, r_code, sx, sy)

    # --------------------------
    # DISTÂNCIA AO FAROL
    # --------------------------
    def distance_to_lighthouse(self):
        ax, ay = self.coord.x, self.coord.y
        lh = self.ambient.getLightHouse().getCoord()
        lx, ly = lh.x, lh.y
        return math.sqrt((lx - ax) ** 2 + (ly - ay) ** 2)

    # --------------------------
    # ESCOLHA DE MOVIMENTO (Q-LEARNING)
    # --------------------------
    def movementChoice(self, sensorDataFront, sensorDataBack,
                       sensorDataLeft, sensorDataRight, sensorDataDirection):
        """
        Integra com Q-Learning:
        - calcula estado a partir dos sensores
        - escolhe ação ε-greedy
        - guarda last_state e last_action
        - devolve a nova coordenada para tentar mover
        """
        state = self.get_state()
        action = choose_action(state)

        self.last_state = state
        self.last_action = action

        dx, dy = ACTIONS[action]
        return Coord.Coord(self.coord.x + dx, self.coord.y + dy)

    # --------------------------
    # MOVER + ATUALIZAR Q
    # --------------------------
    def moveTo(self, newCoord):
        """
        Tenta mover para newCoord, calcula reward e faz update do Q-learning.
        """
        old_dist = self.distance_to_lighthouse()
        reward = 0
        moved = False

        obj = self.ambient.getObject(newCoord)

        # limite fora da grelha
        if obj is not None and getattr(obj, "type", None) == "Limit":
            reward = -25

        # obstáculo interno
        elif isinstance(obj, Obstacle):
            if obj.getType() == "Wall":
                reward = -20
            elif obj.getType() == "Fireplace":
                reward = -10
            else:
                reward = -15

        else:
            # posição livre ou farol ou outro agente (simples)
            # atualizar posição
            self.ambient.occupiedPositions.discard(self.coord.as_tuple())
            self.coord = newCoord
            self.ambient.occupiedPositions.add(self.coord.as_tuple())
            moved = True

            new_dist = self.distance_to_lighthouse()
            lh = self.ambient.getLightHouse().getCoord()

            if self.coord.x == lh.x and self.coord.y == lh.y:
                reward = 100
                self.finished_flag = True
            else:
                if new_dist < old_dist:
                    reward = 5
                else:
                    reward = -10

        # atualizar fitness só para debug
        self.fitness += reward

        # atualizar Q-table
        if self.last_state is not None and self.last_action is not None:
            next_state = self.get_state()
            update_Q(self.last_state, self.last_action, reward, next_state)

        return moved

    # --------------------------
    # EXECUTAR UM PASSO
    # --------------------------
    def executar(self):
        """
        Um passo do agente:
        - lê sensores
        - escolhe movimento via Q-learning (movementChoice)
        - faz moveTo (que atualiza Q)
        """
        f = self.sensorFront()
        b = self.sensorBack()
        l = self.sensorLeft()
        r = self.sensorRight()
        d = self.sensorDirection()

        moveCoord = self.movementChoice(f, b, l, r, d)
        self.moveTo(moveCoord)
