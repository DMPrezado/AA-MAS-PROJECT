# registry.py
TILE_REGISTRY = {}

def register(char):
    def decorator(cls):
        TILE_REGISTRY[char] = cls
        return cls
    return decorator
