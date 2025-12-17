from MapImporter.Registry import TILE_REGISTRY

def render(ambient):
    width, height = ambient.gridDimensions

    # Create empty grid (only size matters)
    grid = [["." for _ in range(width)] for _ in range(height)]

    # Place elements in the grid based on their coordinates
    for element in ambient.elements_list:
        x, y = element.coord.x, element.coord.y
        if 0 <= x < width and 0 <= y < height:
            key = next((k for k, v in TILE_REGISTRY.items() if v == type(element)), "?")
            grid[y][x] = key

    # Print grid
    for row in grid:
        print("".join(row))
