from Coord import Coord
from LightHouse import LightHouse
from LighthouseAmbient import Ambient
from Obstacle import Obstacle
from LighthouseAgent import Agent
import qlearning
import random
import time
from ConfLighthouse import ConfigLightHouse as Conf

# --- HEATMAP ---
import numpy as np
import matplotlib.pyplot as plt


class Simulator:
    def __init__(self):
        # --------------------------
        # Init do ambiente a partir do ficheiro de mapas
        # --------------------------
        self.ambient = Ambient.from_txt(Conf.FILE_EPISODES_INITIAL_POSITIONS)

        # inicializar parâmetros de exploração (ε) a partir da config
        import qlearning as _q
        # Conf pode definir EXPLORATION_*; se não existir, manter defaults
        _q.EPSILON = getattr(Conf, "EXPLORATION_INITIAL", _q.EPSILON)
        _q.EPSILON_MIN = getattr(Conf, "EXPLORATION_FINAL", _q.EPSILON_MIN)
        _q.EPSILON_DECAY = getattr(Conf, "EXPLORATION_DECAY", _q.EPSILON_DECAY)

        # --- MATRIZ DE VISITAS (HEATMAP DO TREINO) ---
        w, h = self.ambient.grid_size
        self.HEATMAP_VISITS = np.zeros((h, w), dtype=int)  # [y][x]

        # cria 1 agente
        start_pos = random.choice(self.ambient.freePositions())
        self.agent = Agent("A0", self.ambient, start_pos)

        self.FITNESS_HISTORY = []

        # --------------------------
        # Treino / Teste / Plot
        # --------------------------
        # Só treina se estiver em Q-learning
        if Conf.MOVE_WITH_QLEARNING:
            self.treinar()
        else:
            print("=== FIXED POLICY: sem treino ===")
            qlearning.EPSILON = 0.0

        # Teste (muitos testes + render a cada passo)
        self.testar()

        # Plot dos resultados da aprendizagem e dos testes (omitido em fixed policy)
        if Conf.MOVE_WITH_QLEARNING:
            self.plot_results()
            self.plot_heatmap()   # heatmap das visitas durante o TREINO


    def reset_agent_random(self, ambient, agent):
        """Reinicia o agente numa posição aleatória livre (sem reset da Q-table)."""
        ambient.occupiedPositions.discard(agent.coord.as_tuple())
        free = ambient.freePositions()
        agent.coord = random.choice(free)
        ambient.occupiedPositions.add(agent.coord.as_tuple())

        agent.finished_flag = False
        agent.prev_pos = None
        agent.fitness = 0


    # run_episode genérico: só conta no heatmap se for passado
    def run_episode(self, ambient, agent, max_steps=80,
                    render_each_step=False, delay=0.1, heatmap=None):
        for t in range(max_steps):
            agent.executar()

            # HEATMAP: contar visita (se heatmap não for None)
            if heatmap is not None:
                heatmap[agent.coord.y, agent.coord.x] += 1

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

        # opcional: garantir que começamos o heatmap a zeros
        self.HEATMAP_VISITS.fill(0)

        for ep in range(N_TRAIN):
            self.reset_agent_random(self.ambient, self.agent)

            # PASSAMOS O HEATMAP AQUI → conta visitas do TREINO
            steps, fit, done = self.run_episode(
                self.ambient, self.agent,
                max_steps=MAX_STEPS_TRAIN,
                render_each_step=Conf.RENDER_DURING_TRAINING,
                heatmap=self.HEATMAP_VISITS
            )

            # Guardar Fitness
            self.FITNESS_HISTORY.append(fit)

            # decair exploração
            qlearning.decay_epsilon()

            # log de vez em quando
            if ep % 20 == 0:
                print(
                    f"Ep {ep:3d} | done={done} | steps={steps:2d} | fitness={fit:4d} | "
                    f"epsilon={qlearning.EPSILON:.3f} | Q={len(qlearning.Q_TABLES['lighthouse'])}"
                )


    def testar(self):
        print("\n=== TESTE (policy aprendida) ===")

        # no teste queremos a política greedy
        qlearning.EPSILON = 0.0

        N_TEST = Conf.N_TEST
        MAX_STEPS_TEST = 50

        total_fitness = 0
        wins = 0

        self.ambient.init_render_window()

        for test_i in range(N_TEST):
            self.reset_agent_random(self.ambient, self.agent)

            print(f"\n--- TESTE {test_i+1}/{N_TEST} ---")

            # AQUI **NÃO** PASSAMOS HEATMAP → não mexe na matriz
            steps, fit, done = self.run_episode(
                self.ambient, self.agent,
                max_steps=MAX_STEPS_TEST,
                render_each_step=True,
                delay=0.10
            )

            total_fitness += fit
            wins += 1 if done else 0

            print(f"\nResultado teste {test_i+1}: done={done} | steps={steps} | fitness_final={fit}")

        print("\n=== RESUMO TESTES ===")
        print(f"Chegou ao farol: {wins}/{N_TEST}")
        print(f"Fitness média: {total_fitness / N_TEST:.2f}")


    def plot_results(self):
        plt.figure()
        plt.plot(self.FITNESS_HISTORY)
        plt.title("Lighthouse: Fitness ao longo dos episódios de treino")
        plt.xlabel("Episódio")
        plt.ylabel("Fitness")
        plt.grid()
        plt.show()


    # HEATMAP com obstáculos a preto + farol marcado
    def plot_heatmap(self):
        visits = self.HEATMAP_VISITS.copy()

        plt.figure()
        plt.title("Heatmap de visitas (TREINO) – Lighthouse")
        plt.xlabel("x")
        plt.ylabel("y")

        # Heatmap base
        plt.imshow(visits, origin="upper")
        plt.colorbar(label="Nº de visitas")

        # Obstáculos a preto
        for o in self.ambient.obstacles:
            x, y = o.getCoord().x, o.getCoord().y
            plt.scatter(x, y, marker="s", s=300, c="black")

        # Farol (objetivo)
        lh = self.ambient.getLightHouse().getCoord()
        plt.scatter(lh.x, lh.y, marker="*", s=250)

        plt.show()


if __name__ == "__main__":
    Simulator()
