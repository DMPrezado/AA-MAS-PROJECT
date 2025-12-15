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

    # ------------------------
    # TRAINING
    # ------------------------
    NUMBER_EPISODES = 2000
    MAX_STEPS_PER_EPISODE = 120
    RENDER_DURING_TRAINING = False

    # ------------------------
    # STEP SENSOR
    # ------------------------
    FRONT_SENSOR_MAX_DIST = 4

    # ------------------------
    # BASE COST
    # ------------------------
    STEP_COST = -0.2

    # ------------------------
    # REWARDS / PENALTIES
    # ------------------------
    REWARD_PICK_RESOURCE = 80
    REWARD_DROP_IN_NEST  = 200

    REWARD_HIT_WALL_OR_LIMIT = -10
    REWARD_IN_FIREPLACE      = -30

    # ações inválidas (não bloqueia — só ensina)
    REWARD_INVALID_PICK = -5
    REWARD_INVALID_DROP = -5

    # penalizações a cada 5 passos (leves)
    PENALTY_5_STEPS_NO_PICKUP = -2
    PENALTY_5_STEPS_CARRYING  = -3

    # shaping (aproximar/afastar do alvo)
    REWARD_MOVE_CLOSER_TARGET = 2
    REWARD_MOVE_AWAY_TARGET   = -2
