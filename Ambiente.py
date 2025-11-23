# Ambient
#     Attributes:
#         - agents: list[Agent]
#         - obstacles: list[Obstacle]
#         - lighthouse: LightHouse
#         - grid_size (or bounds): tuple[int,int] / whatever represents limits
#     Methods:
#  David  :(   - freePositions() -> list[Coord]
#    :)   - getLightHouse() -> LightHouse
#    :)   - getAgentsList() -> list[Agent]
#  Manuel  :(   - render() -> str (render)


import Coord


class Ambiente:
    def __init__(self, agents, obstacles, lighthouse, grid_size):
        self.agents = agents  # list of Agent objects
        self.obstacles = obstacles  # list of Obstacle objects
        self.lighthouse = lighthouse  # LightHouse object
        self.grid_size = grid_size  # tuple (width, height)

    def freePositions(self):
        # Returns a list of free positions (Coord objects) in the environment
        free_positions = []
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                coord = Coord(x, y)
                ########
                # TODO: verificar se a posiçao está ocupada por um agente, obstáculo ou farol
                ########
        return free_positions

    def getLightHouse(self):
        return self.lighthouse

    def getAgentsList(self):
        return self.agents
    
    def render(self):
        # Returns a string representation of the environment
        grid = [['.' for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
        
        for obstacle in self.obstacles:
            coord = obstacle.getCoord()
            grid[coord.y][coord.x] = '#'
        
        lighthouse_coord = self.lighthouse.getCoord()
        grid[lighthouse_coord.y][lighthouse_coord.x] = 'L'
        
        for agent in self.agents:
            coord = agent.getCoord()
            grid[coord.y][coord.x] = 'A'
        
        return '\n'.join(' '.join(row) for row in grid)