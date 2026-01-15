# ForagingSimulator.py
import random
import time
from Resource import Resource
import qlearning
from ForagingAmbient import ForagingAmbient
from ForagingAgent import ForagingAgent
from ConfForaging import ConfigForaging as Conf

# --- NOVO: imports para heatmap ---
import numpy as np
import matplotlib.pyplot as plt


class ForagingSimulator:
    def __init__(self):
        self.ambient = ForagingAmbient.from_txt(Conf.FILE_EPISODES_MAP)

        # inicializar parâmetros de exploração (ε) a partir da config
        import qlearning as _q
        _q.EPSILON = Conf.EXPLORATION_INITIAL
        _q.EPSILON_MIN = Conf.EXPLORATION_FINAL
        _q.EPSILON_DECAY = Conf.EXPLORATION_DECAY

        # --- NOVO: matriz de visitas (heatmap) ---
        w, h = self.ambient.grid_size
        self.HEATMAP_VISITS = np.zeros((h, w), dtype=int)  # [y][x]

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

        # Apenas plotar resultados se estivermos em Q-learning (modo fixed não deve abrir GUI)
        if Conf.MOVE_WITH_QLEARNING:
            self.plot_results()
            self.plot_heatmap()  # --- NOVO: mostra heatmap no fim ---


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


    # --- ALTERADO: run_episode recebe heatmap e conta visitas ---
    def run_episode(self, max_steps, render=False, delay=0.08, heatmap=None):
        for t in range(max_steps):
            self.agent.executar()

            # contar visita (depois do passo)
            if heatmap is not None:
                heatmap[self.agent.coord.y, self.agent.coord.x] += 1

            if render and hasattr(self.ambient, "root") and self.ambient.root.winfo_exists():
                self.ambient.render_window()
                self.ambient.root.update_idletasks()
                self.ambient.root.update()
                time.sleep(delay)

            if self.agent.finished_flag:
                return (t + 1, self.agent.fitness, True)

        return (max_steps, self.agent.fitness, False)


    def treinar(self):
        print("=== TREINO FORAGING ===")
        for ep in range(Conf.NUMBER_EPISODES):
            # recarregar mapa para episódios limpos
            self.ambient = ForagingAmbient.from_txt(Conf.FILE_EPISODES_MAP)
            self.ambient.agents = []
            start = random.choice(self.ambient.freePositions())
            self.agent = ForagingAgent("F0", self.ambient, start)

            for _ in range(Conf.NUMBER_RESOURCES):
                randPosition = random.choice(self.ambient.freePositions())
                self.ambient.resources.append(Resource(randPosition))
                # garantir que o ambient conhece a posição ocupada pelo recurso
                try:
                    self.ambient.occupiedPositions.add(randPosition.as_tuple())
                except Exception:
                    self.ambient.occupiedPositions.add((randPosition.x, randPosition.y))

            steps, fit, done = self.run_episode(
                max_steps=Conf.MAX_STEPS_PER_EPISODE,
                render=Conf.RENDER_DURING_TRAINING
            )

            # guarda fitness
            self.FITNESS_HISTORY.append(fit)

            qlearning.decay_epsilon()

            if ep % 25 == 0:
                print(
                    f"Ep {ep:3d} | done={done} | steps={steps:3d} | fitness={fit:7.1f} | "
                    f"epsilon={qlearning.EPSILON:.3f} | Q={len(qlearning.Q_TABLES['foraging'])}"
                )


    def testar(self):
        print("\n=== TESTE FORAGING (policy aprendida) ===")
        qlearning.EPSILON = 0.0

        # --- NOVO: reset do heatmap (para ser só dos testes) ---
        self.HEATMAP_VISITS.fill(0)

        N_TEST = 2
        total = 0
        wins = 0

        for i in range(N_TEST):
            self.ambient = ForagingAmbient.from_txt(Conf.FILE_EPISODES_MAP)
            self.ambient.agents = []
            start = random.choice(self.ambient.freePositions())
            self.agent = ForagingAgent("F0", self.ambient, start)

            for _ in range(Conf.NUMBER_RESOURCES):
                randPosition = random.choice(self.ambient.freePositions())
                self.ambient.resources.append(Resource(randPosition))
                try:
                    self.ambient.occupiedPositions.add(randPosition.as_tuple())
                except Exception:
                    self.ambient.occupiedPositions.add((randPosition.x, randPosition.y))

            self.ambient.init_render_window()
            print(f"\n--- TESTE {i+1}/{N_TEST} ---")

            # --- ALTERADO: passa heatmap para contar visitas ---
            steps, fit, done = self.run_episode(
                max_steps=Conf.MAX_STEPS_PER_EPISODE,
                render=True,
                delay=0.08,
                heatmap=self.HEATMAP_VISITS
            )

            total += fit
            if done:
                wins += 1

            print(f"Resultado teste {i+1}: done={done} | steps={steps} | fitness_final={fit}")

        print("\n=== RESUMO TESTES ===")
        print(f"Recursos recolhidos todos em testes: {wins}/{N_TEST}")
        print(f"Fitness média: {total / N_TEST:.2f}")


    def plot_results(self):
        plt.figure()
        plt.plot(self.FITNESS_HISTORY)
        plt.title("Foraging: Fitness ao longo dos episódios de treino")
        plt.xlabel("Episódio")
        plt.ylabel("Fitness")
        plt.grid()
        plt.show()


    # --- NOVO: heatmap com obstáculos a preto ---
    def plot_heatmap(self):
        visits = self.HEATMAP_VISITS.copy()

        plt.figure()
        plt.title("Heatmap de visitas (TESTE) – Foraging")
        plt.xlabel("x")
        plt.ylabel("y")

        # heatmap base
        plt.imshow(visits, origin="upper")
        plt.colorbar(label="Nº de visitas")

        # obstáculos a preto (Wall/Fireplace/etc.)
        for o in self.ambient.obstacles:
            x, y = o.getCoord().x, o.getCoord().y
            plt.scatter(x, y, marker="s", s=300, c="black")

        # ninho (marcador por cima)
        if self.ambient.getNest() is not None:
            n = self.ambient.getNest().getCoord()
            plt.scatter(n.x, n.y, marker="s", s=250)

        plt.show()


if __name__ == "__main__":
    ForagingSimulator()
