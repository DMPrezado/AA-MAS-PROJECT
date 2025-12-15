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

        # spawn do agente
        if hasattr(self.ambient, "agent_spawns") and self.ambient.agent_spawns:
            start_pos = random.choice(self.ambient.agent_spawns)
        else:
            start_pos = random.choice(self.ambient.freePositions())

        self.agent = ForagingAgent("F0", self.ambient, start_pos)

        self.treinar()
        self.testar()

    def reset_episode(self):
        # reposicionar agente
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

        # NOTA: aqui não estamos a “resetar” recursos; se quiseres episódios independentes,
        # podes recarregar o mapa a cada episódio.
        # Para já mantemos simples e determinístico.

    def run_episode(self, max_steps, render=False, delay=0.08):
        for t in range(max_steps):
            self.agent.executar()

            if render:
                print(f"\nStep {t} | fitness={self.agent.fitness} | has_resource={self.agent.has_resource} | dir={self.agent.whereIsFront}")
                print(self.ambient.render())
                time.sleep(delay)

        return self.agent.fitness

    def treinar(self):
        print("=== TREINO FORAGING ===")
        for ep in range(Conf.NUMBER_EPISODES):
            # para episódios “limpos” com recursos repostos, o melhor é recarregar o mapa:
            self.ambient = ForagingAmbient.from_txt(Conf.FILE_EPISODES_MAP)
            # re-ligar agente ao novo ambiente
            self.ambient.agents = []
            start = random.choice(self.ambient.freePositions())
            self.agent = ForagingAgent("F0", self.ambient, start)

            fit = self.run_episode(
                max_steps=Conf.MAX_STEPS_PER_EPISODE,
                render=Conf.RENDER_DURING_TRAINING
            )
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

            print(f"\n--- TESTE {i+1}/{N_TEST} ---")
            print(self.ambient.render())
            fit = self.run_episode(max_steps=Conf.MAX_STEPS_PER_EPISODE, render=True, delay=0.08)
            total += fit
            print(f"Resultado: fitness={fit}")

        print("\n=== RESUMO TESTES ===")
        print(f"Fitness média: {total / N_TEST:.2f}")

if __name__ == "__main__":
    ForagingSimulator()
