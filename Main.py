# main.py

from Coord import Coord
from LightHouse import LightHouse
from Ambient import Ambient
from Obstacle import Obstacle
from Agent import Agent
from qlearning import Q
import random
import time


def reset_agent_random(ambient, agent):
    ambient.occupiedPositions.discard(agent.coord.as_tuple())
    free = ambient.freePositions()
    pos = random.choice(free)
    agent.coord = pos
    ambient.occupiedPositions.add(pos.as_tuple())
    agent.finished_flag = False


def main():
    width, height = 8, 6
    lighthouse = LightHouse(Coord(6, 4))

    obstacles = [
        Obstacle(Coord(3, 1), "Wall"),
        Obstacle(Coord(3, 2), "Wall"),
        Obstacle(Coord(3, 3), "Wall"),
        Obstacle(Coord(1, 4), "Fireplace"),
    ]

    ambient = Ambient([], obstacles, lighthouse, (width, height))

    # criar um agente numa posição livre aleatória
    start_pos = random.choice(ambient.freePositions())
    agent = Agent("A0", ambient, start_pos)

    N_EPISODES = 30
    MAX_STEPS = 40

    for ep in range(N_EPISODES):
        reset_agent_random(ambient, agent)
        print(f"\n=== Episódio {ep} ===")
        for t in range(MAX_STEPS):
            agent.executar()
            print(ambient.render())
            print(f"fitness: {agent.fitness}")
            time.sleep(0.05)
            if agent.finished_flag:
                print(f"Chegou ao farol em {t+1} passos!")
                break

    print("\nTamanho da Q-table aprendida:", len(Q))


if __name__ == "__main__":
    main()
