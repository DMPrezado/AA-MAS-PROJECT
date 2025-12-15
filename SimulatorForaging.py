# ForagingSimulator.py
import random
import time
import qlearning
from ForagingAmbient import ForagingAmbient
from ForagingAgent import ForagingAgent
from ConfForaging import ConfigForaging as Conf

class ForagingSimulator:
    def __init__(self):
        self.ambient = ForagingAmbient.from_txt(Conf.FILE_EPISODES_MAP)

        start_pos = random.choice(self.ambient.freePositions())
        self.agent = ForagingAgent("F0", self.ambient, start_pos)

        self.FITNESS_HISTORY = []


        # Só treina se estiver em Q-learning
        if Conf.MOVE_WITH_QLEARNING:
            self.treinar()
        else:
            print("=== FIXED POLICY: sem treino ===")
            qlearning.EPSILON = 0.0

        # Teste (sempre)
        self.testar()

        self.plot_results()

    def reset_episode(self):
        self.ambient.occupiedPositions.discard(self.agent.coord.as_tuple())
        self.agent.coord = random.choice(self.ambient.freePositions())
        self.ambient.occupiedPositions.add(self.agent.coord.as_tuple())

        self.agent.fitness = 0
        self.agent.finished_flag = False
        self.agent.has_resource = False
        self.agent.steps_since_pickup = 0
        self.agent.steps_carrying = 0
        self.agent.whereIsFront = (0, -1)
        self.agent.last_state = None
        self.agent.last_action = None

    def run_episode(self, max_steps, render=False, delay=0.08):
        for t in range(max_steps):
            self.agent.executar()

            if render and hasattr(self.ambient, "root") and self.ambient.root.winfo_exists():
                self.ambient.render_window()
                self.ambient.root.update_idletasks()
                self.ambient.root.update()
                time.sleep(delay)

        return self.agent.fitness

    def treinar(self):
        print("=== TREINO FORAGING ===")
        for ep in range(Conf.NUMBER_EPISODES):
            # recarregar mapa para episódios limpos
            self.ambient = ForagingAmbient.from_txt(Conf.FILE_EPISODES_MAP)
            self.ambient.agents = []
            start = random.choice(self.ambient.freePositions())
            self.agent = ForagingAgent("F0", self.ambient, start)

            fit = self.run_episode(
                max_steps=Conf.MAX_STEPS_PER_EPISODE,
                render=Conf.RENDER_DURING_TRAINING
            )

            #gaurda fitness
            self.FITNESS_HISTORY.append(fit)

            qlearning.decay_epsilon()

            if ep % 25 == 0:
                print(f"Ep {ep:3d} | fitness={fit:7.1f} | epsilon={qlearning.EPSILON:.3f}")

    def testar(self):
        print("\n=== TESTE FORAGING (policy aprendida) ===")
        qlearning.EPSILON = 0.0

        N_TEST = 2
        total = 0


        for i in range(N_TEST):
            self.ambient = ForagingAmbient.from_txt(Conf.FILE_EPISODES_MAP)
            self.ambient.agents = []
            start = random.choice(self.ambient.freePositions())
            self.agent = ForagingAgent("F0", self.ambient, start)

            self.ambient.init_render_window()
            print(f"\n--- TESTE {i+1}/{N_TEST} ---")
            fit = self.run_episode(max_steps=Conf.MAX_STEPS_PER_EPISODE, render=True, delay=0.08)
            total += fit
            print(f"Resultado: fitness={fit}")

        print("\n=== RESUMO TESTES ===")
        print(f"Fitness média: {total / N_TEST:.2f}")

    def plot_results(self):
        import matplotlib.pyplot as plt

        plt.plot(self.FITNESS_HISTORY)
        plt.title("Fitness ao longo dos episódios de treino")
        plt.xlabel("Episódio")
        plt.ylabel("Fitness")
        plt.grid()
        plt.show()


if __name__ == "__main__":
    ForagingSimulator()
