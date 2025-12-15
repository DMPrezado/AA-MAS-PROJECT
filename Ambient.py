# Ambient.py

import Coord
from LightHouse import LightHouse
from Obstacle import Obstacle

class Ambient:
    def __init__(self, grid_size, lighthouse=None, obstacles=None, agents=None):
        self.grid_size = grid_size  # (width, height)
        self.lighthouse = lighthouse
        self.obstacles = obstacles if obstacles is not None else []
        self.agents = agents if agents is not None else []

        # posições ocupadas
        self.occupiedPositions = set()
        self._rebuild_occupied()

    def _rebuild_occupied(self):
        self.occupiedPositions.clear()

        for o in self.obstacles:
            self.occupiedPositions.add(o.getCoord().as_tuple())

        if self.lighthouse is not None:
            self.occupiedPositions.add(self.lighthouse.getCoord().as_tuple())

        for a in self.agents:
            self.occupiedPositions.add(a.getCoord().as_tuple())

    # --------------------------
    # GETTERS
    # --------------------------
    def getLightHouse(self):
        return self.lighthouse

    def getAgentsList(self):
        return self.agents

    # --------------------------
    # POSIÇÕES LIVRES
    # --------------------------
    def freePositions(self):
        free_positions = []
        width, height = self.grid_size

        for x in range(width):
            for y in range(height):
                if (x, y) not in self.occupiedPositions:
                    free_positions.append(Coord.Coord(x, y))
        return free_positions

    # --------------------------
    # UTIL: coord -> tuple
    # --------------------------
    def _coord_to_tuple(self, coord):
        if isinstance(coord, Coord.Coord):
            return coord.getX(), coord.getY()
        elif isinstance(coord, tuple):
            return coord
        else:
            raise TypeError("coord deve ser Coord ou (x,y)")

    # --------------------------
    # OBJETO NUMA POSIÇÃO
    # --------------------------
    def getObject(self, coord):
        x, y = self._coord_to_tuple(coord)
        width, height = self.grid_size

        # fora da grelha
        if x < 0 or y < 0 or x >= width or y >= height:
            class LimitObj:
                type = "Limit"
                def getType(self): return "Limit"
            return LimitObj()

        # farol
        if self.lighthouse is not None and self.lighthouse.getCoord().as_tuple() == (x, y):
            return self.lighthouse

        # agentes
        for a in self.agents:
            if a.getCoord().as_tuple() == (x, y):
                return a

        # obstáculos
        for o in self.obstacles:
            if o.getCoord().as_tuple() == (x, y):
                return o

        return None

    # --------------------------
    # RENDER
    # --------------------------
    def render(self):
        width, height = self.grid_size
        grid = [['.' for _ in range(width)] for _ in range(height)]

        for obstacle in self.obstacles:
            c = obstacle.getCoord()
            x, y = c.getX(), c.getY()
            t = obstacle.getType() if hasattr(obstacle, "getType") else getattr(obstacle, "type", None)

            if t == "Wall":
                grid[y][x] = "W"
            elif t == "Fireplace":
                grid[y][x] = "F"
            elif t in ("Limit", "Border"):
                grid[y][x] = "B"
            else:
                grid[y][x] = "#"

        if self.lighthouse is not None:
            c = self.lighthouse.getCoord()
            grid[c.getY()][c.getX()] = "L"

        for a in self.agents:
            c = a.getCoord()
            grid[c.getY()][c.getX()] = "\033[92mA\033[0m"

        return "\n".join(" ".join(row) for row in grid)

    # ==========================================================
    #      CRIAÇÃO DO MAPA DENTRO DO AMBIENTE
    # ==========================================================

    @staticmethod
    def from_txt(filename):
        """
        Carrega um mapa ASCII do ficheiro:
          . = empty
          L = lighthouse
          A = agent
          W = wall
          F = fireplace
          B = border/limit (obstáculo tipo Limit) [opcional]
        """
        with open(filename, "r", encoding="utf-8") as f:
            raw_lines = [line.rstrip("\n") for line in f if line.strip()]

        if not raw_lines:
            raise ValueError("O ficheiro do mapa está vazio.")

        height = len(raw_lines)
        width = len(raw_lines[0])

        for line in raw_lines:
            if len(line) != width:
                raise ValueError("Mapa não retangular: linhas com comprimentos diferentes.")

        obstacles = []
        lighthouse = None
        agent_spawns = []

        for y, line in enumerate(raw_lines):
            for x, ch in enumerate(line):
                coord = Coord.Coord(x, y)

                if ch == "W":
                    obstacles.append(Obstacle(coord, "Wall"))
                elif ch == "F":
                    obstacles.append(Obstacle(coord, "Fireplace"))
                elif ch == "B":
                    obstacles.append(Obstacle(coord, "Limit"))
                elif ch == "L":
                    lighthouse = LightHouse(coord)
                elif ch == "A":
                    agent_spawns.append(coord)
                else:
                    # vazio ou desconhecido
                    pass

        ambient = Ambient(grid_size=(width, height), lighthouse=lighthouse, obstacles=obstacles, agents=[])

        # guardamos as posições iniciais possíveis para o main usar
        ambient.agent_spawns = agent_spawns
        return ambient

    @staticmethod
    def demo_map():
        """
        Mapa de teste “hard-coded” mas agora dentro do Ambient (não no main).
        """
        width, height = 10, 8
        lighthouse = LightHouse(Coord.Coord(8, 6))

        obstacles = [
            Obstacle(Coord.Coord(4, 1), "Wall"),
            Obstacle(Coord.Coord(4, 2), "Wall"),
            Obstacle(Coord.Coord(4, 3), "Wall"),
            Obstacle(Coord.Coord(4, 4), "Wall"),
            Obstacle(Coord.Coord(2, 6), "Fireplace"),
        ]

        return Ambient(grid_size=(width, height), lighthouse=lighthouse, obstacles=obstacles, agents=[])
