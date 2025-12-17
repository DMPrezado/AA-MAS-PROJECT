from MapImporter.Registry import register


@register("A")
class Agent:
    def __init__(self, coord):
        self.coord = coord
