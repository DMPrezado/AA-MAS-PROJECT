from Coord import Coord
from LightHouse import LightHouse
from Ambient import Ambient
from Obstacle import Obstacle
import Agent
import random
import time



# Ensure Agent instances expose getCoord (Ambient.render/getObject expect it)
if not hasattr(Agent.Agent, "getCoord"):
    def _agent_getCoord(self):
        return self.coord
    Agent.Agent.getCoord = _agent_getCoord

def create_agent_without_init(name, ambient, coord):
    """
    Create an Agent instance without calling its broken __init__.
    Set minimal attributes used by movementChoice/moveTo/render.
    """
    a = object.__new__(Agent.Agent)
    a.name = name
    a.finished_flag = False
    a.ambient = ambient
    a.coord = coord
    a.fitness = 0
    a.whereIsFront = (0, -1)  # default facing up
    # register agent in ambient
    ambient.agents.append(a)
    ambient.occupiedPositions.add(coord.as_tuple())
    return a

def main():
    width, height = 6, 5
    lighthouse = LightHouse(Coord(2, 2))
    obstacles = [
        Obstacle(Coord(0, 0)),
        Obstacle(Coord(5, 4)),
    ]

    ambient = Ambient([], obstacles, lighthouse, (width, height))

    # create 3 agents at random free positions
    free = ambient.freePositions()
    random.shuffle(free)
    agents = []
    for i in range(3):
        if not free:
            break
        pos = free.pop()
        a = create_agent_without_init(f"A{i}", ambient, pos)
        agents.append(a)

    steps = 10
    for t in range(steps):
        print(f"\nStep {t}")
        # each agent picks a random allowed move (movementChoice uses ambient.freePositions())
        for a in list(ambient.agents):
            try:
                move = a.movementChoice(None, None, None, None, None)
            except TypeError:
                # fallback: pick random neighbor manually
                possible = [
                    Coord(a.coord.x + 1, a.coord.y),
                    Coord(a.coord.x - 1, a.coord.y),
                    Coord(a.coord.x, a.coord.y + 1),
                    Coord(a.coord.x, a.coord.y - 1),
                ]
                free_pos = ambient.freePositions()
                free_set = {c.as_tuple() for c in free_pos}
                candidates = [m for m in possible if m.as_tuple() in free_set]
                move = random.choice(candidates) if candidates else a.coord
            # perform move
            try:
                a.moveTo(move)
            except Exception as e:
                # todo ignora erros para já
                pass


        # print grid
        print(ambient.render())
        time.sleep(0.2)

if __name__ == "__main__":
    main()
