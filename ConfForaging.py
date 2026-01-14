class ConfigForaging:
    # ------------------------
    # EXECUTION MODE
    # ------------------------
    MODE = "qlearning"   # "fixed" | "qlearning"
    MOVE_WITH_FIXED_POLICIES = (MODE == "fixed")
    MOVE_WITH_QLEARNING     = (MODE == "qlearning")

    # ------------------------
    # MAP FILE
    # ------------------------
    FILE_EPISODES_MAP = "maps/foraging_map1.txt"
    #FILE_EPISODES_MAP = "maps/foraging_map_large.txt"

    # ------------------------
    # TRAINING
    # ------------------------
    NUMBER_EPISODES = 1500
    MAX_STEPS_PER_EPISODE = 700
    RENDER_DURING_TRAINING = False
    NUMBER_RESOURCES = 4
    WALL_PERCENTAGE = 0.1 #NEW

    # ------------------------
    # STEP SENSOR
    # ------------------------
    FRONT_SENSOR_MAX_DIST = 4

    # ------------------------
    # BASE COST
    # ------------------------
    STEP_COST = -0.06

    # ------------------------
    # REWARDS / PENALTIES
    # ------------------------
    REWARD_PICK_RESOURCE = 40
    REWARD_DROP_IN_NEST  = 100

    REWARD_HIT_WALL_OR_LIMIT = -5
    REWARD_IN_FIREPLACE      = -20

    # ações inválidas (não bloqueia — só ensina)
    REWARD_INVALID_PICK = -5
    REWARD_INVALID_DROP = -5

    # penalizações a cada 5 passos (leves)
    PENALTY_5_STEPS_NO_PICKUP = -10
    PENALTY_5_STEPS_CARRYING  = -8

    # shaping (aproximar/afastar do alvo)
    REWARD_MOVE_CLOSER_TARGET = 4
    REWARD_MOVE_AWAY_TARGET   = -2
