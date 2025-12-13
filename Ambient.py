# Ambient.py

import Coord
from Obstacle import Obstacle
from LightHouse import LightHouse


class Ambient:
    def __init__(self, agents, obstacles, lighthouse, grid_size):
        """
        agents: lista de Agent
        obstacles: lista de Obstacle (type: 'Wall', 'Fireplace', 'Limit'/'Border')
        lighthouse: LightHouse
        grid_size: (width, height)
        """
        self.agents = agents
        self.obstacles = obstacles
        self.lighthouse = lighthouse
        self.grid_size = grid_size  # (width, height)

        # posições ocupadas por qualquer coisa dentro da grelha
        self.occupiedPositions = set()

        for agent in agents:
            self.occupiedPositions.add(agent.getCoord().as_tuple())

        for obstacle in obstacles:
            self.occupiedPositions.add(obstacle.getCoord().as_tuple())

        if lighthouse is not None:
            self.occupiedPositions.add(lighthouse.getCoord().as_tuple())

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
    # GETTERS
    # --------------------------
    def getLightHouse(self):
        return self.lighthouse

    def getAgentsList(self):
        return self.agents

    # --------------------------
    # UTIL: coordenada -> tuplo
    # --------------------------
    def _coord_to_tuple(self, coord):
        if isinstance(coord, Coord.Coord):
            return coord.getX(), coord.getY()
        elif isinstance(coord, tuple):
            return coord
        else:
            raise TypeError("coord deve ser Coord ou (x,y)")

    # --------------------------
    # OBTÉM OBJETO NA COORDENADA
    # --------------------------
    def getObject(self, coord):
        """
        Devolve o objeto (Agent, Obstacle, LightHouse ou um 'objeto limite') numa dada coordenada.
        Usado pelos sensores e pelo moveTo do Agent.
        """
        x, y = self._coord_to_tuple(coord)
        width, height = self.grid_size

        # fora dos limites da grelha -> tratar como 'Limit'
        if x < 0 or y < 0 or x >= width or y >= height:
            class LimitObj:
                type = "Limit"

                def getType(self):
                    return "Limit"

            return LimitObj()

        # farol
        if self.lighthouse is not None and self.lighthouse.getCoord().as_tuple() == (x, y):
            return self.lighthouse

        # agentes
        for a in self.agents:
            if a.getCoord().as_tuple() == (x, y):
                return a

        # obstáculos (walls, fireplaces, borders)
        for o in self.obstacles:
            if o.getCoord().as_tuple() == (x, y):
                return o

        # nada nessa posição
        return None

    # --------------------------
    # RENDER ASCII
    # --------------------------
    def render(self):
        """
        Representação visual da grelha:
          .  = empty
          L  = lighthouse
          A  = agent
          W  = wall
          F  = fireplace
          B  = border / limit (se houver obstaculos deste tipo no interior da grelha)
        """

        width, height = self.grid_size
        grid = [['.' for _ in range(width)] for _ in range(height)]

        # obstáculos (Walls, Fireplaces, Borders)
        for obstacle in self.obstacles:
            c = obstacle.getCoord()
            x, y = c.getX(), c.getY()

            obj_type = obstacle.getType()

            if obj_type == "Wall":
                grid[y][x] = 'W'
            elif obj_type == "Fireplace":
                grid[y][x] = 'F'
            elif obj_type in ("Limit", "Border"):
                grid[y][x] = 'B'
            else:
                grid[y][x] = '#'

        # farol
        if self.lighthouse is not None:
            c = self.lighthouse.getCoord()
            grid[c.getY()][c.getX()] = 'L'

        # agentes
        for agent in self.agents:
            c = agent.getCoord()
            grid[c.getY()][c.getX()] = 'A'

        return '\n'.join(' '.join(row) for row in grid)

    # --------------------------
    # CARREGAR DE TXT (opcional)
    # --------------------------
    @staticmethod
    def from_txt(filename):
        """
        Lê um txt onde:
          . = empty
          L = lighthouse
          A = agent
          W = wall
          F = fireplace
          B = border / limit (obstáculo do tipo 'Limit')
        """
        with open(filename, 'r') as f:
            raw_lines = [line.rstrip('\n') for line in f if line.strip()]

        if not raw_lines:
            raise ValueError("O ficheiro está vazio.")

        height = len(raw_lines)
        width = len(raw_lines[0])

        for line in raw_lines:
            if len(line) != width:
                raise ValueError("Todas as linhas do mapa precisam ter o mesmo comprimento.")

        agents_temp = []
        obstacles = []
        lighthouse = None

        for y, line in enumerate(raw_lines):
            for x, ch in enumerate(line):
                coord = Coord.Coord(x, y)

                if ch == 'W':
                    obstacles.append(Obstacle(coord, "Wall"))
                elif ch == 'F':
                    obstacles.append(Obstacle(coord, "Fireplace"))
                elif ch == 'B':
                    obstacles.append(Obstacle(coord, "Limit"))
                elif ch == 'L':
                    lighthouse = LightHouse(coord)
                elif ch == 'A':
                    agents_temp.append((f"A{x}_{y}", coord))
                # '.' é vazio

        ambient = Ambient([], obstacles, lighthouse, (width, height))

        from Agent import Agent  # import local para evitar ciclos
        real_agents = []
        for name, coord in agents_temp:
            a = Agent(name, ambient, coord)
            real_agents.append(a)

        ambient.agents = real_agents
        ambient.occupiedPositions = set()

        for o in obstacles:
            ambient.occupiedPositions.add(o.getCoord().as_tuple())
        if lighthouse:
            ambient.occupiedPositions.add(lighthouse.getCoord().as_tuple())
        for a in real_agents:
            ambient.occupiedPositions.add(a.getCoord().as_tuple())

        return ambient
