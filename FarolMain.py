from Coord import Coord
from Ambient import Ambient
from LightHouse import LightHouse
from Obstacle import Obstacle
from Agent import Agent
import random
import time


def main():
    # parâmetros do mapa
    width, height = 6, 5
    max_steps = 100
    step_delay = 0.08

    # criar farol e alguns obstáculos de exemplo
    lighthouse = LightHouse(Coord(2, 2))
    obstacles = [
        Obstacle(Coord(1, 1), "Wall"),
        Obstacle(Coord(4, 3), "Fireplace"),
    ]

    # criar o ambiente (usar argumentos nomeados para evitar confusões)
    ambient = Ambient(grid_size=(width, height), lighthouse=lighthouse, obstacles=obstacles, agents=[])

    # inicializar janela gráfica (se disponível)
    try:
        ambient.init_render_window()
    except Exception:
        pass

    # escolher duas posições livres para os agentes
    free = ambient.freePositions()
    if len(free) < 2:
        print("Não há posições livres suficientes para criar 2 agentes.")
        return

    random.shuffle(free)
    a0_pos = free.pop()
    a1_pos = free.pop()

    # instanciar agentes usando o construtor oficial
    a0 = Agent("A0", ambient, a0_pos)
    a1 = Agent("A1", ambient, a1_pos)

    # imprimir estado inicial no terminal (TUI) e também usar GUI
    print("Farol ambiente inicial:")
    print(ambient.render())

    directions = [ (0,0), (1,0), (-1,0), (0,1), (0,-1) ]  # stay, E, W, S, N

    for t in range(max_steps):
        print(f"\nStep {t+1}")

        # para cada agente, escolher movimento aleatório
        for agent in list(ambient.agents):
            # posição atual
            x, y = agent.getCoord().getX(), agent.getCoord().getY()

            # gera lista de candidatos válidos (evita limites/obstáculos)
            candidates = []
            for dx, dy in directions:
                nc = Coord(x + dx, y + dy)
                obj = ambient.getObject(nc)

                # se for limite/fora do mapa ou obstáculo do tipo Wall/Fireplace/Limit, ignorar
                if obj is not None:
                    # objeto limite criado dinamicamente por Ambient tem type="Limit"
                    tpe = getattr(obj, "type", None)
                    if tpe == "Limit":
                        continue
                    # se for obstáculo e tiver getType()
                    if hasattr(obj, "getType"):
                        ot = obj.getType()
                        if ot in ("Wall", "Fireplace", "Limit"):
                            continue
                # caso contrário, aceitar (permite sobreposição entre agentes)
                candidates.append(nc)

            if not candidates:
                # sem candidatos válidos -> fica parado
                continue

            chosen = random.choice(candidates)

            try:
                agent.moveTo(chosen)
            except Exception:
                # ignorar erros por agente para manter a simulação a correr
                pass

            # se atingiu o farol, moveTo deverá marcar finished_flag
            if getattr(agent, "finished_flag", False):
                print(f"Agente {agent.name} atingiu o farol na posição {agent.getCoord()} no passo {t+1}.")
                print(ambient.render())
                # imprimir fitness de todos os agentes antes de terminar
                print("\nFitness final dos agentes:")
                for ag in ambient.agents:
                    print(f" - {ag.name}: {getattr(ag, 'fitness', 0)}")
                return

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

        # se o utilizador fechou a janela, abortar a simulação e imprimir motivo+fitness
        if getattr(ambient, "window_closed", False):
            print("Simulação interrompida: janela fechada pelo utilizador.")
            print("\nFitness final dos agentes:")
            for ag in ambient.agents:
                print(f" - {ag.name}: {getattr(ag, 'fitness', 0)}")
            return

        time.sleep(step_delay)

    print("Parado: limite de passos atingido sem chegar ao farol.")
    # imprimir fitness final dos agentes quando o limite de passos é atingido
    print("\nFitness final dos agentes:")
    for ag in ambient.agents:
        print(f" - {ag.name}: {getattr(ag, 'fitness', 0)}")


if __name__ == "__main__":
    main()

