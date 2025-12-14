# Ambient.py

import Coord
from LightHouse import LightHouse

class Ambient:
    def __init__(self, agents, obstacles, lighthouse, grid_size):
        self.agents = agents
        self.obstacles = obstacles
        self.lighthouse = lighthouse
        self.grid_size = grid_size  # (width, height)

        self.occupiedPositions = set()

        for agent in agents:
            self.occupiedPositions.add(agent.getCoord().as_tuple())

        for obstacle in obstacles:
            self.occupiedPositions.add(obstacle.getCoord().as_tuple())

        if lighthouse is not None:
            self.occupiedPositions.add(lighthouse.getCoord().as_tuple())

    def freePositions(self):
        free_positions = []
        width, height = self.grid_size

        for x in range(width):
            for y in range(height):
                if (x, y) not in self.occupiedPositions:
                    free_positions.append(Coord.Coord(x, y))
        return free_positions

    def getLightHouse(self):
        return self.lighthouse

    def getAgentsList(self):
        return self.agents

    def _coord_to_tuple(self, coord):
        if isinstance(coord, Coord.Coord):
            return coord.getX(), coord.getY()
        elif isinstance(coord, tuple):
            return coord
        else:
            raise TypeError("coord deve ser Coord ou (x,y)")

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

    def render(self):
        width, height = self.grid_size
        grid = [['.' for _ in range(width)] for _ in range(height)]

        # obstáculos
        for obstacle in self.obstacles:
            c = obstacle.getCoord()
            x, y = c.getX(), c.getY()
            t = getattr(obstacle, "type", None)

            if t == "Wall":
                grid[y][x] = "W"
            elif t == "Fireplace":
                grid[y][x] = "F"
            elif t in ("Limit", "Border"):
                grid[y][x] = "B"
            else:
                grid[y][x] = "#"

        # farol
        if self.lighthouse is not None:
            c = self.lighthouse.getCoord()
            grid[c.getY()][c.getX()] = "L"

        # agentes
        for a in self.agents:
            c = a.getCoord()
            grid[c.getY()][c.getX()] = "A"

        return "\n".join(" ".join(row) for row in grid)
