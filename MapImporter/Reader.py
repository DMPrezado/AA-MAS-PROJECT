# reader.py
from MapImporter.Factory import create_tile
import Coord

def read_map(path):
    with open(path, "r", encoding="utf-8") as f:
            raw_lines = [line.rstrip("\n") for line in f if line.strip()]

    if not raw_lines:
        raise ValueError("O ficheiro do mapa está vazio.")

    height = len(raw_lines)
    width = len(raw_lines[0])

    for line in raw_lines:
        if len(line) != width:
            raise ValueError("Mapa não retangular: linhas com comprimentos diferentes.")
    
    
    grid = []

    with open(path, "r", encoding="utf-8") as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                if char == " ":
                    break
                
                if char == ".":
                    continue

                obj = create_tile(char, Coord.Coord(x, y))
                if obj:
                    grid.append(obj)

    return grid, (width, height)
