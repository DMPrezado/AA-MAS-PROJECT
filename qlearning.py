# qlearning.py

import random

# 4 ações possíveis
ACTIONS = {
    0: (0, -1),  # up
    1: (0,  1),  # down
    2: (-1, 0),  # left
    3: (1,  0),  # right
}

# Q-table: (state_tuple, action) -> Q-value
Q = {}

ALPHA = 0.2   # taxa de aprendizagem
GAMMA = 0.95  # desconto futuro
EPSILON = 0.1 # ε-greedy


def get_Q(state, action):
    return Q.get((state, action), 0.0)


def choose_action(state):
    """Política ε-greedy."""
    if random.random() < EPSILON:
        # exploração
        return random.choice(list(ACTIONS.keys()))
    else:
        # exploração: escolhe ação com maior Q
        qs = [(a, get_Q(state, a)) for a in ACTIONS.keys()]
        max_q = max(qs, key=lambda t: t[1])[1]
        best_actions = [a for a, q in qs if q == max_q]
        return random.choice(best_actions)


def update_Q(state, action, reward, next_state):
    """Equação clássica de Q-learning."""
    sa = (state, action)
    old_q = Q.get(sa, 0.0)

    max_next_q = max(
        (get_Q(next_state, a) for a in ACTIONS.keys()),
        default=0.0
    )

    new_q = old_q + ALPHA * (reward + GAMMA * max_next_q - old_q)
    Q[sa] = new_q
