# Entities.py
from Registry import register

@register("W")
class Wall:
    pass

@register("F")
class Fireplace:
    pass

@register("N")
class Nest:
    pass

@register("R")
class Resource:
    pass

@register("A")
class Agent:
    pass

@register("#")
class Obstacle:
    pass

@register("L")
class LightHouse: 
    pass

@register("B")
class Limit:
    pass
    
@register(".")
class Empty:
    pass
