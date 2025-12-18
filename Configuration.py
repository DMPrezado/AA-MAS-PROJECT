

selected_problem = "lighthouse"     # choose lighthouse or foraging

mode = "qlearning"     # choose qlearning or fixed

MOVE_WITH_QLEARNING = (mode == "qlearning")
MOVE_WITH_FIXED_POLICIES = (mode == "fixed")


class LightHouse:
    # ------------------------
    # TRAINING PARAMETERS
    # ------------------------
    MAX_STEPS = 20
    MAX_TRAINING_EPISODES = 200
    
    
    # ------------------------
    # MAPS
    # ------------------------
    MAPS_PATHS = [
        "maps\maps1.txt",
        "maps\maps2.txt",
        "maps\maps3.txt",
        "maps\maps4.txt",
        "maps\maps5.txt",
        "maps\maps6.txt",
        "maps\maps7.txt",
        "maps\maps8.txt",
    ]
    
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
    
    