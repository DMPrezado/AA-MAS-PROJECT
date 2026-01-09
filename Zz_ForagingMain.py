"""
Zz_ForagingMain.py
Simulação simples para Foraging (smoke test):
- cria um ForagingAmbient corretamente
- cria 2 agentes em posições livres
- cada passo os agentes escolhem uma ação aleatória (move/pick/drop)
- actualiza a janela Tkinter (se disponível)
- para quando não houver recursos ou quando N passos for atingido
- imprime o fitness final dos agentes

Esta versão evita alterar outros ficheiros do projecto.
"""

from Coord import Coord
from ForagingAmbient import ForagingAmbient
from ForagingAgent import ForagingAgent, FORAGING_ACTIONS
from Nest import Nest
from Resource import Resource
from Obstacle import Obstacle
import random
import time


def main():
    # parâmetros do mapa
    width, height = 8, 6
    max_steps = 120
    step_delay = 0.06

    # criar ninho, recursos e alguns obstáculos de exemplo
    nest = Nest(Coord(1, 1))
    resources = [Resource(Coord(5, 2)), Resource(Coord(6, 4)), Resource(Coord(2, 3))]
    obstacles = [
        Obstacle(Coord(3, 1), "Wall"),
        Obstacle(Coord(4, 3), "Fireplace"),
    ]

    # criar o ambiente foraging
    ambient = ForagingAmbient(grid_size=(width, height), nest=nest, obstacles=obstacles, resources=resources, agents=[])

    # inicializar janela gráfica (se disponível)
    try:
        ambient.init_render_window()
    except Exception:
        pass

    # escolher duas posições livres para os agentes
    free = ambient.freePositions()
    if len(free) < 2:
        print("Não há posições livres suficientes para criar 2 agentes foraging.")
        return

    random.shuffle(free)
    a0_pos = free.pop()
    a1_pos = free.pop()

    # instanciar agentes
    a0 = ForagingAgent("F0", ambient, a0_pos)
    a1 = ForagingAgent("F1", ambient, a1_pos)

    print("Ambiente foraging inicial:")

    actions = list(FORAGING_ACTIONS.keys())

    # imprimir estado inicial no terminal
    print(ambient.render())

    for t in range(max_steps):
        print(f"\nStep {t+1}")

        # cada agente escolhe uma ação aleatória (inclui PICK/DROP)
        for agent in list(ambient.agents):
            action = random.choice(actions)
            try:
                # usar apply_action para que a lógica de recompensas seja aplicada
                agent.apply_action(action)
            except Exception:
                # ignorar erros por agente para manter a simulação a correr
                pass

        # imprimir o estado do ambiente no terminal (TUI)
        print(ambient.render())

        # actualizar janela gráfica se estiver aberta
        if hasattr(ambient, "root") and ambient.root.winfo_exists():
            try:
                ambient.render_window()
                ambient.root.update_idletasks()
                ambient.root.update()
            except Exception:
                pass

        # se o utilizador fechou a janela, abortar a simulação e imprimir motivo + fitness
        if getattr(ambient, "window_closed", False):
            print("Simulação interrompida: janela fechada pelo utilizador.")
            print("\nFitness final dos agentes:")
            for ag in ambient.agents:
                print(f" - {ag.name}: {getattr(ag, 'fitness', 0)}")
            return

        # condição de paragem: todos os recursos recolhidos
        if not ambient.resources:
            print(f"Parado: todos os recursos recolhidos no passo {t+1}.")
            print("\nFitness final dos agentes:")
            for ag in ambient.agents:
                print(f" - {ag.name}: {getattr(ag, 'fitness', 0)}")
            return

        time.sleep(step_delay)

    print("Parado: limite de passos atingido sem recolher todos os recursos.")
    print("\nFitness final dos agentes:")
    for ag in ambient.agents:
        print(f" - {ag.name}: {getattr(ag, 'fitness', 0)}")


if __name__ == "__main__":
    main()

