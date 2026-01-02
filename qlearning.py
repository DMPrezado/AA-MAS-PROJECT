# qlearning.py
import random



class qlearning: 
    
    # ------------------------------------------------------------
    # AÇÕES default (Lighthouse usa isto)
    # ------------------------------------------------------------
    ACTIONS = {
        0: (0, -1),  # up
        1: (0,  1),  # down
        2: (-1, 0),  # left
        3: (1,  0),  # right
    }
    
    def __init__(self):    
        # ------------------------------------------------------------
        # Q-TABLES separadas por tarefa (não mistura Lighthouse/Foraging)
        # ------------------------------------------------------------
        self.Q_TABLES = {
            "lighthouse": {},  # (state, action) -> q
            "foraging": {},    # (state, action) -> q
        }

   

    # ------------------------------------------------------------
    # Hiperparâmetros globais
    # ------------------------------------------------------------
    ALPHA = 0.2
    GAMMA = 0.95

    EPSILON = 1.0
    EPSILON_MIN = 0.05
    EPSILON_DECAY = 0.995


    def _get_qtable(task: str):
        """Devolve a Q-table da tarefa, criando se necessário."""
        if task not in Q_TABLES:
            Q_TABLES[task] = {}
        return Q_TABLES[task]


    def get_Q(state, action, task="lighthouse"):
        Q = _get_qtable(task)
        return Q.get((state, action), 0.0)


    def choose_action(state, actions=None, banned_actions=None, task="lighthouse"):
        """
        Política ε-greedy genérica.
        - actions: lista de ações possíveis (ex.: [0,1,2,3] ou [0..5])
                se None, usa ACTIONS.keys() (modo Lighthouse)
        - banned_actions: set de ações a evitar (opcional)
        - task: "lighthouse" / "foraging"
        """
        if actions is None:
            actions = list(ACTIONS.keys())

        if banned_actions is None:
            banned_actions = set()

        actions = [a for a in actions if a not in banned_actions]
        if not actions:
            actions = list(ACTIONS.keys())

        # exploração
        if random.random() < EPSILON:
            return random.choice(actions)

        # greedy
        qs = [(a, get_Q(state, a, task=task)) for a in actions]
        max_q = max(qs, key=lambda t: t[1])[1]
        best = [a for a, q in qs if q == max_q]
        return random.choice(best)


    def update_Q(state, action, reward, next_state, actions=None, task="lighthouse"):
        """
        Q(s,a) <- Q(s,a) + α [r + γ max_a' Q(s',a') - Q(s,a)]
        - actions: lista de ações possíveis do problema
        """
        if actions is None:
            actions = list(ACTIONS.keys())

        Q = _get_qtable(task)

        old_q = Q.get((state, action), 0.0)
        max_next_q = max((get_Q(next_state, a, task=task) for a in actions), default=0.0)

        Q[(state, action)] = old_q + ALPHA * (reward + GAMMA * max_next_q - old_q)


    def decay_epsilon():
        global EPSILON
        EPSILON = max(EPSILON_MIN, EPSILON * EPSILON_DECAY)


    def reset_task(task: str):
        Q_TABLES[task] = {}
