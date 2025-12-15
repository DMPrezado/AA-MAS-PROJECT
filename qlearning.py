# qlearning.py

import random

ACTIONS = {
    0: (0, -1),  # up
    1: (0,  1),  # down
    2: (-1, 0),  # left
    3: (1,  0),  # right
}

Q = {}

ALPHA = 0.2
GAMMA = 0.95

EPSILON = 1.0
EPSILON_MIN = 0.05
EPSILON_DECAY = 0.995


def get_Q(state, action):
    return Q.get((state, action), 0.0)


def choose_action(state, banned_actions=None):
    if banned_actions is None:
        banned_actions = set()

    actions = [a for a in ACTIONS.keys() if a not in banned_actions]
    if not actions:
        actions = list(ACTIONS.keys())

    # exploração
    if random.random() < EPSILON:
        return random.choice(actions)

    # exploração
    qs = [(a, get_Q(state, a)) for a in actions]
    max_q = max(qs, key=lambda t: t[1])[1]
    best = [a for a, q in qs if q == max_q]
    return random.choice(best)


def update_Q(state, action, reward, next_state):
    old_q = Q.get((state, action), 0.0)
    max_next_q = max((get_Q(next_state, a) for a in ACTIONS.keys()), default=0.0)
    Q[(state, action)] = old_q + ALPHA * (reward + GAMMA * max_next_q - old_q)


def decay_epsilon():
    global EPSILON
    EPSILON = max(EPSILON_MIN, EPSILON * EPSILON_DECAY)
