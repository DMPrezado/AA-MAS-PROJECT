# Entities.py
from MapImporter.Registry import register

'''Agent entity should not be here because of its complexity'''


'''WARNING: REWARDS NEED TO BE ON AN ACCESSIBLE PLACE TO CHANGE THEM EASILY'''
'''WARNING: COLORS OF EACH CLASS NEED TO BE DEFINED ON THE CLASS ITSELF'''


# -----------------------
# Lighthouse
# -----------------------
@register("L")
class LightHouse: 
    def __init__(self,coord):
        self.coord = coord
        self.reward = 100
        self.obstacle = False
        self.REWARD_STEP_CLOSER = 10
        self.REWARD_STEP_AWAY = -15


# -----------------------
# Foraging
# -----------------------
@register("N")
class Nest:
    def __init__(self,coord):
        self.coord = coord
        self.reward = 100
        self.obstacle = False

@register("R")
class Resource:
    def __init__(self,coord):
        self.coord = coord
        self.reward = 50
        self.obstacle = False



# -----------------------
# Common Entities
# -----------------------
@register("W")
class Wall:
    def __init__(self,coord):
        self.coord = coord
        self.reward = -10
        self.obstacle = True

@register("F")
class Fireplace:
    def __init__(self,coord):
        self.coord = coord
        self.reward = -20
        self.obstacle = True



    
