# factory.py
from Registry import TILE_REGISTRY

def create_tile(char):
    cls = TILE_REGISTRY.get(char)
    return cls() if cls else None
