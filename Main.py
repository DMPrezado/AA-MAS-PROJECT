# Main.py

from Coord import Coord
from LightHouse import LightHouse
from Ambient import Ambient
from Obstacle import Obstacle
from Agent import Agent
import qlearning
import random
import time


def reset_agent_random(ambient, agent):
    """Reinicia o agente numa posição aleatória livre (sem reset da Q-table)."""
    ambient.occupiedPositions.discard(agent.coord.as_tuple())
    free = ambient.freePositions()
    agent.coord = random.choice(free)
    ambient.occupiedPositions.add(agent.coord.as_tuple())

    agent.finished_flag = False
    agent.prev_pos = None
    agent.fitness = 0


def run_episode(ambient, agent, max_steps=80, render_each_step=False, delay=0.05):
    """Executa 1 episódio e devolve (steps_usados, fitness_final, chegou_ao_farol)."""
    for t in range(max_steps):
        agent.executar()

        if render_each_step:
            print(f"\nStep {t} | fitness={agent.fitness}")
            print(ambient.render())
            time.sleep(delay)

        if agent.finished_flag:
            return (t + 1, agent.fitness, True)

    return (max_steps, agent.fitness, False)


def main():
    # --------------------------
    # CONFIG DO MAPA
    # --------------------------
    width, height = 10, 8
    lighthouse = LightHouse(Coord(8, 6))

    obstacles = [
        Obstacle(Coord(4, 1), "Wall"),
        Obstacle(Coord(4, 2), "Wall"),
        Obstacle(Coord(4, 3), "Wall"),
        Obstacle(Coord(4, 4), "Wall"),
        Obstacle(Coord(2, 6), "Fireplace"),
        Obstacle(Coord(6, 6), "Fireplace"),
    ]

    ambient = Ambient([], obstacles, lighthouse, (width, height))

    # cria 1 agente
    start_pos = random.choice(ambient.freePositions())
    agent = Agent("A0", ambient, start_pos)

    # --------------------------
    # 1) TREINO
    # --------------------------
    N_TRAIN = 400
    MAX_STEPS_TRAIN = 80

    print("=== TREINO ===")
    for ep in range(N_TRAIN):
        reset_agent_random(ambient, agent)
        steps, fit, done = run_episode(
            ambient, agent,
            max_steps=MAX_STEPS_TRAIN,
            render_each_step=False
        )

        # decair exploração
        qlearning.decay_epsilon()

        # log de vez em quando
        if ep % 20 == 0:
            print(f"Ep {ep:3d} | done={done} | steps={steps:2d} | fitness={fit:4d} | epsilon={qlearning.EPSILON:.3f} | Q={len(qlearning.Q)}")

    # --------------------------
    # 2) TESTE (muitos testes + render a cada passo)
    # --------------------------
    print("\n=== TESTE (policy aprendida) ===")

    # IMPORTANTÍSSIMO: no teste queremos a política "fixa"
    qlearning.EPSILON = 0.0

    N_TEST = 10
    MAX_STEPS_TEST = 50

    total_fitness = 0
    wins = 0

    for test_i in range(N_TEST):
        reset_agent_random(ambient, agent)

        print(f"\n--- TESTE {test_i+1}/{N_TEST} ---")
        print("Estado inicial:")
        print(ambient.render())

        steps, fit, done = run_episode(
            ambient, agent,
            max_steps=MAX_STEPS_TEST,
            render_each_step=True,   # <- volta a mostrar movimentos como antes
            delay=0.10               # ajusta a velocidade
        )

        total_fitness += fit
        wins += 1 if done else 0

        print(f"\nResultado teste {test_i+1}: done={done} | steps={steps} | fitness_final={fit}")

    print("\n=== RESUMO TESTES ===")
    print(f"Chegou ao farol: {wins}/{N_TEST}")
    print(f"Fitness média: {total_fitness / N_TEST:.2f}")


if __name__ == "__main__":
    main()
