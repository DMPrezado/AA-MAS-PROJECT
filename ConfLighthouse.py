# ConfLighthouse.py

class ConfigLightHouse:

    # ------------------------
    # EXECUTION MODE
    # ------------------------
    # "fixed"      -> política fixa (heurística)
    # "qlearning"  -> aprendizagem Q-learning
    MODE = "qlearning"   # ALTERA AQUI ou via terminal (ver SimulatorLighthouse.py)

    MOVE_WITH_FIXED_POLICIES = (MODE == "fixed")
    MOVE_WITH_QLEARNING = (MODE == "qlearning")

    # ------------------------
    # MAP FILES
    # ------------------------
    #FILE_EPISODES_INITIAL_POSITIONS = "maps/initial_positions1.txt"
    #FILE_TEST_INITIAL_POSITIONS = "maps/initial_positions1.txt"
    FILE_EPISODES_INITIAL_POSITIONS = "maps/lighthouse_map1.txt"
    FILE_TEST_INITIAL_POSITIONS = "maps/lighthouse_map1.txt"

    # ------------------------
    # TRAINING PARAMETERS
    # ------------------------
    NUMBER_EPISODES = 600
    #MAX_STEPS_PER_EPISODE = 200 #problemas pequenos
    MAX_STEPS_PER_EPISODE = 400  #problemas/mapas grandes
    RENDER_DURING_TRAINING = False
    N_TEST = 10

    # ------------------------
    # Q-LEARNING PARAMETERS
    # ------------------------
    EXPLORATION_INITIAL = 1.0
    EXPLORATION_FINAL = 0.1
    EXPLORATION_DECAY = 0.995

    # ------------------------
    # REWARDS
    # ------------------------
    REWARD_REACH_GOAL = 1000
    REWARD_STEP_CLOSER = 1
    REWARD_STEP_AWAY = -2
    REWARD_HIT_WALL = -5
    REWARD_IN_FIREPLACE = -15
    REWARD_HIT_OBJECT = -5
