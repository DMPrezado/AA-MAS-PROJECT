




"""
    Configuration for LightHouse problem
"""

class ConfigLightHouse:
        
    FILE_EPISODES_INITIAL_POSITIONS = "maps/initial_positions1.txt"
    FILE_TEST_INITIAL_POSITIONS = "maps/initial_positions1.txt"
    
    MOVE_WITH_QLEARNING = False
    MOVE_WITH_FIXED_POLICIES = True



     # Training parameters
    NUMBER_EPISODES = 20
    MAX_STEPS_PER_EPISODE = 100
    RENDER_DURING_TRAINING = False

    # Q-LEARNING parameters
    EXPLORATION_INITIAL = 1.0
    EXPLORATION_FINAL = 0.1
    EXPLORATION_DECAY = 0.995

   

    # Rewards
    REWARD_REACH_GOAL = 100
    REWARD_STEP_CLOSER = 10     ##e se perdesse em todos os passos mas menos quando se aproxima?
    REWARD_STEP_AWAY = -15
    REWARD_HIT_WALL = -10
    REWARD_IN_FIREPLACE = -30
    REWARD_HIT_OBJECT = -10
