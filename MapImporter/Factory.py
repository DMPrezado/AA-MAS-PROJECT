# factory.py
from MapImporter.Registry import TILE_REGISTRY

def create_tile(char, coord):
    cls = TILE_REGISTRY.get(char)
    return cls(coord) if cls else None