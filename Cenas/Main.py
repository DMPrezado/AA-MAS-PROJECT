# Main.py

import random
import time

import qlearning
from LighthouseAgent import LighthouseAgent
from LighthouseAmbient import LighthouseAmbient

"""
    Precisamos de importar:
        - Receber o mada de um txt ambient.import_from_txt(...)
        - Definir numero de episódios de treino
        - Máximo de passos por episódio
        - Rewards definidos
        - Politicas fixas
"""






def reset_agent_random(ambient, agent):
    ambient.occupiedPositions.discard(agent.coord.as_tuple())
    agent.coord = random.choice(ambient.freePositions())
    ambient.occupiedPositions.add(agent.coord.as_tuple())
    agent.finished_flag = False
    agent.fitness = 0

def run_episode(ambient, agent, max_steps, render=False, delay=0.08):
    for t in range(max_steps):
        agent.executar()
        if render:
            print(f"\nStep {t} | fitness={agent.fitness}")
            print(ambient.render())
            time.sleep(delay)
        if agent.finished_flag:
            return t + 1, agent.fitness, True
    return max_steps, agent.fitness, False

def main():
    # 1) criar mapa dentro do ambiente
    ambient = LighthouseAmbient.demo_map()
    agent = LighthouseAgent("A0", ambient, random.choice(ambient.freePositions()))

    # 2) TREINO
    N_TRAIN = 200
    for ep in range(N_TRAIN):
        reset_agent_random(ambient, agent)
        run_episode(ambient, agent, max_steps=80, render=False)
        qlearning.decay_epsilon()

    # 3) TESTE (mostrar movimentos)
    qlearning.EPSILON = 0.0
    for i in range(5):
        reset_agent_random(ambient, agent)
        print(f"\n--- TESTE {i+1} ---")
        print(ambient.render())
        run_episode(ambient, agent, max_steps=60, render=True)

if __name__ == "__main__":
    main()
