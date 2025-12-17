# reader.py
from Factory import create_tile

def read_map(path):
    grid = []

    with open(path, "r", encoding="utf-8") as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                if char == ".":
                    continue

                obj = create_tile(char)
                if obj:
                    grid.append((x, y, obj))

    return grid
