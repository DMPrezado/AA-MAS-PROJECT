# Conf.py

class ConfigLightHouse:

    # ------------------------
    # EXECUTION MODE
    # ------------------------
    # "fixed"      -> política fixa (heurística)
    # "qlearning"  -> aprendizagem Q-learning
    MODE = "qlearning"   # ALTERA AQUI ou via terminal (ver Simulator.py)

    MOVE_WITH_FIXED_POLICIES = (MODE == "fixed")
    MOVE_WITH_QLEARNING = (MODE == "qlearning")

    # ------------------------
    # MAP FILES
    # ------------------------
    FILE_EPISODES_INITIAL_POSITIONS = "maps/initial_positions1.txt"
    FILE_TEST_INITIAL_POSITIONS = "maps/initial_positions1.txt"

    # ------------------------
    # TRAINING PARAMETERS
    # ------------------------
    NUMBER_EPISODES = 200
    MAX_STEPS_PER_EPISODE = 100
    RENDER_DURING_TRAINING = False

    # ------------------------
    # Q-LEARNING PARAMETERS
    # ------------------------
    EXPLORATION_INITIAL = 1.0
    EXPLORATION_FINAL = 0.1
    EXPLORATION_DECAY = 0.995

    # ------------------------
    # REWARDS
    # ------------------------
    REWARD_REACH_GOAL = 100
    REWARD_STEP_CLOSER = 10
    REWARD_STEP_AWAY = -15
    REWARD_HIT_WALL = -10
    REWARD_IN_FIREPLACE = -30
    REWARD_HIT_OBJECT = -10
