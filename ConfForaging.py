class ConfigForaging:
    # ------------------------
    # EXECUTION MODE
    # ------------------------
    MODE = "qlearning"   # "fixed" | "qlearning"
    #MODE = "fixed"
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
    NUMBER_EPISODES = 700
    MAX_STEPS_PER_EPISODE = 1000
    RENDER_DURING_TRAINING = False
    NUMBER_RESOURCES = 3

    # ------------------------
    # STEP SENSOR
    # ------------------------
    FRONT_SENSOR_MAX_DIST = 4

    # ------------------------
    # EXPLORATION (ε-greedy)
    # ------------------------
    EXPLORATION_INITIAL = 1.0
    EXPLORATION_FINAL = 0.2
    EXPLORATION_DECAY = 0.995

    # ------------------------
    # BASE COST
    # ------------------------
    # custo base por passo: ligeiramente maior para desencorajar movimentos inúteis
    STEP_COST = -0.10

    # ------------------------
    # REWARDS / PENALTIES
    # ------------------------
    REWARD_PICK_RESOURCE = 100
    REWARD_DROP_IN_NEST  = 500

    REWARD_HIT_WALL_OR_LIMIT = -5
    REWARD_IN_FIREPLACE      = -20

    # ações inválidas (não bloqueia — só ensina)
    REWARD_INVALID_PICK = -5
    REWARD_INVALID_DROP = -5

    # penalizações a cada 5 passos (leves)
    # torna a penalização por falta de progresso mais severa (dissuadir ficar a oscilar)
    PENALTY_5_STEPS_NO_PICKUP = -6
    PENALTY_5_STEPS_CARRYING  = -2

    # shaping (aproximar/afastar do alvo)
    # seguir a lógica do Lighthouse: recompensa leve por aproximar, pena mais forte por afastar
    REWARD_MOVE_CLOSER_TARGET = 1
    REWARD_MOVE_AWAY_TARGET   = -2

    # penalidade para movimentos de ida-e-volta (oscilações)
    PENALTY_REPEAT_MOVE = -3
