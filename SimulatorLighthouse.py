from Coord import Coord
from LightHouse import LightHouse
from Ambient import Ambient
from Obstacle import Obstacle
from Agent import Agent
import qlearning
import random
import time
from Conf import ConfigLightHouse as Conf


class SimulatorLighthouse:
    def __init__(self):
        # # --------------------------
        # # Init do ambiente a partir do ficheiro de mapas
        # # --------------------------
        self.ambient = Ambient.from_txt(Conf.FILE_EPISODES_INITIAL_POSITIONS)

        # cria 1 agente
        start_pos = random.choice(self.ambient.freePositions())
        self.agent = Agent("A0", self.ambient, start_pos)

        self.FITNESS_HISTORY = []


        # --------------------------
        # 1) TREINO
        # --------------------------
        self.treinar()
        # --------------------------
        # 2) TESTE (muitos testes + render a cada passo)
        # --------------------------
        self.testar()
        # --------------------------
        # 3) Plot dos resultados da aprendizagem e dos testes.
        # --------------------------
        #TODO: implementar plotagem dos resultados
        self.plot_results()
        
        
    def reset_agent_random(self, ambient, agent):
        """Reinicia o agente numa posição aleatória livre (sem reset da Q-table)."""
        ambient.occupiedPositions.discard(agent.coord.as_tuple())
        free = ambient.freePositions()
        agent.coord = random.choice(free)
        ambient.occupiedPositions.add(agent.coord.as_tuple())

        agent.finished_flag = False
        agent.prev_pos = None
        agent.fitness = 0

    def run_episode(self, ambient, agent, max_steps=80, render_each_step=False, delay=0.1):
        for t in range(max_steps):
            agent.executar()

            if render_each_step and hasattr(self.ambient, "root") and self.ambient.root.winfo_exists():
                self.ambient.render_window()
                self.ambient.root.update_idletasks()
                self.ambient.root.update()
                time.sleep(delay)


            if agent.finished_flag:
                return (t + 1, agent.fitness, True)

        return (max_steps, agent.fitness, False)


    def treinar(self):
        N_TRAIN = Conf.NUMBER_EPISODES
        MAX_STEPS_TRAIN = Conf.MAX_STEPS_PER_EPISODE

        print("=== TREINO ===")
        for ep in range(N_TRAIN):
            self.reset_agent_random(self.ambient, self.agent)
            steps, fit, done = self.run_episode(
                self.ambient, self.agent,
                max_steps=MAX_STEPS_TRAIN,
                render_each_step=Conf.RENDER_DURING_TRAINING
            )

            ##Guardar Fitness
            self.FITNESS_HISTORY.append(fit)

            # decair exploração
            qlearning.decay_epsilon()

            # log de vez em quando
            if ep % 20 == 0:
                print(f"Ep {ep:3d} | done={done} | steps={steps:2d} | fitness={fit:4d} | epsilon={qlearning.EPSILON:.3f} | Q={len(qlearning.Q_TABLES["lighthouse"])}")

    def testar(self):
        print("\n=== TESTE (policy aprendida) ===")

        # IMPORTANTÍSSIMO: no teste queremos a política "fixa"
        qlearning.EPSILON = 0.0

        N_TEST = 10
        MAX_STEPS_TEST = 50

        total_fitness = 0
        wins = 0

        self.ambient.init_render_window()

        for test_i in range(N_TEST):
            self.reset_agent_random(self.ambient, self.agent)

            print(f"\n--- TESTE {test_i+1}/{N_TEST} ---")
            # print("Estado inicial:")
            # print(self.ambient.render())
            steps, fit, done = self.run_episode(
                self.ambient, self.agent,
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


    def plot_results(self):
        import matplotlib.pyplot as plt

        plt.plot(self.FITNESS_HISTORY)
        plt.title("Lighthouse: Fitness ao longo dos episódios de treino")
        plt.xlabel("Episódio")
        plt.ylabel("Fitness")
        plt.grid()
        plt.show()




if __name__ == "__main__":
    SimulatorLighthouse()
