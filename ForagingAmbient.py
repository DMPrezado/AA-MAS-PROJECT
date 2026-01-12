# ForagingAmbient.py
import Coord
from Obstacle import Obstacle
from Nest import Nest
from Resource import Resource

class ForagingAmbient:
    def __init__(self, grid_size, nest=None, obstacles=None, resources=None, agents=None):
        self.grid_size = grid_size
        self.nest = nest
        self.obstacles = obstacles if obstacles is not None else []
        self.resources = resources if resources is not None else []
        self.picked_resources = 0
        self.agents = agents if agents is not None else []

        self.occupiedPositions = set()
        self._rebuild_occupied()

    def _rebuild_occupied(self):
        self.occupiedPositions.clear()
        for o in self.obstacles:
            self.occupiedPositions.add(o.getCoord().as_tuple())
        if self.nest is not None:
            self.occupiedPositions.add(self.nest.getCoord().as_tuple())
        for r in self.resources:
            self.occupiedPositions.add(r.getCoord().as_tuple())
        for a in self.agents:
            self.occupiedPositions.add(a.getCoord().as_tuple())

    def _coord_to_tuple(self, coord):
        if isinstance(coord, Coord.Coord):
            return coord.getX(), coord.getY()
        elif isinstance(coord, tuple):
            return coord
        else:
            raise TypeError("coord deve ser Coord ou (x,y)")

    def getNest(self):
        return self.nest

    def freePositions(self):
        free_positions = []
        w, h = self.grid_size
        for x in range(w):
            for y in range(h):
                if (x, y) not in self.occupiedPositions:
                    free_positions.append(Coord.Coord(x, y))
        return free_positions

    def remove_resource_at(self, coord):
        x, y = self._coord_to_tuple(coord)
        for i, r in enumerate(self.resources):
            if r.getCoord().as_tuple() == (x, y):
                self.resources.pop(i)
                self.occupiedPositions.discard((x, y))
                return True
        return False

    def getObject(self, coord):
        x, y = self._coord_to_tuple(coord)
        w, h = self.grid_size
        if x < 0 or y < 0 or x >= w or y >= h:
            class LimitObj:
                type = "Limit"
                def getType(self): return "Limit"
            return LimitObj()
        if self.nest is not None and self.nest.getCoord().as_tuple() == (x, y):
            return self.nest
        for r in self.resources:
            if r.getCoord().as_tuple() == (x, y):
                return r
        for a in self.agents:
            if a.getCoord().as_tuple() == (x, y):
                return a
        for o in self.obstacles:
            if o.getCoord().as_tuple() == (x, y):
                return o
        return None

    def has_resource_at(self, coord):
        x, y = self._coord_to_tuple(coord)
        for r in self.resources:
            if r.getCoord().as_tuple() == (x, y):
                return True
        return False

    def render(self):
        w, h = self.grid_size
        grid = [['.' for _ in range(w)] for _ in range(h)]
        for o in self.obstacles:
            c = o.getCoord()
            x, y = c.getX(), c.getY()
            t = o.getType() if hasattr(o, "getType") else getattr(o, "type", None)
            if t == "Wall":
                grid[y][x] = "W"
            elif t == "Fireplace":
                grid[y][x] = "F"
            else:
                grid[y][x] = "#"
        if self.nest is not None:
            c = self.nest.getCoord()
            grid[c.getY()][c.getX()] = "N"
        for r in self.resources:
            c = r.getCoord()
            grid[c.getY()][c.getX()] = "R"
        for a in self.agents:
            c = a.getCoord()
            grid[c.getY()][c.getX()] = "\033[92mA\033[0m"
        return "\n".join(" ".join(row) for row in grid)

    @staticmethod
    def from_txt(filename):
        with open(filename, "r", encoding="utf-8") as f:
            raw_lines = [line.rstrip("\n") for line in f if line.strip()]
        if not raw_lines:
            raise ValueError("O ficheiro do mapa está vazio.")
        height = len(raw_lines)
        width = len(raw_lines[0])
        for line in raw_lines:
            if len(line) != width:
                raise ValueError("Mapa não retangular.")
        obstacles = []
        resources = []
        nest = None
        agent_spawns = []
        for y, line in enumerate(raw_lines):
            for x, ch in enumerate(line):
                coord = Coord.Coord(x, y)
                if ch == "W":
                    obstacles.append(Obstacle(coord, "Wall"))
                elif ch == "F":
                    obstacles.append(Obstacle(coord, "Fireplace"))
                # elif ch == "R":
                #     resources.append(Resource(coord))
                elif ch == "N":
                    nest = Nest(coord)
                elif ch == "A":
                    agent_spawns.append(coord)
        ambient = ForagingAmbient(
            grid_size=(width, height),
            nest=nest,
            obstacles=obstacles,
            resources=resources,
            agents=[]
        )
        ambient.agent_spawns = agent_spawns

        return ambient

    # -------------------- RENDER WINDOW --------------------
    def init_render_window(self):
        import tkinter as tk
        if hasattr(self, "root") and self.root.winfo_exists():
            return
        self.window_closed = False
        self.CELL = 30
        w, h = self.grid_size
        self.root = tk.Tk()
        self.root.title("Foraging Grid")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.canvas = tk.Canvas(
            self.root,
            width=w * self.CELL,
            height=h * self.CELL,
            bg="white"
        )
        self.canvas.pack()

    def _on_close(self):
        self.window_closed = True
        self.root.destroy()

    def render_window(self):
        if not hasattr(self, "root") or not self.root.winfo_exists():
            return
        self.canvas.delete("all")
        c = self.CELL
        width, height = self.grid_size

        def draw_cell(x, y, color, text=None):
            self.canvas.create_rectangle(
                x*c, y*c, (x+1)*c, (y+1)*c,
                fill=color, outline="gray"
            )
            if text:
                self.canvas.create_text(
                    x*c + c/2, y*c + c/2,
                    text=text, font=("Arial", 12, "bold")
                )

        # fundo
        for y in range(height):
            for x in range(width):
                draw_cell(x, y, "white")

        # obstáculos
        for o in self.obstacles:
            coord = o.getCoord()
            t = o.getType()
            color = {
                "Wall": "black",
                "Fireplace": "orange",
                "Limit": "gray",
                "Border": "gray"
            }.get(t, "brown")
            draw_cell(coord.getX(), coord.getY(), color)

        # ninho
        if self.nest:
            c0 = self.nest.getCoord()
            draw_cell(c0.getX(), c0.getY(), "blue", "N")

        # recursos
        for r in self.resources:
            c0 = r.getCoord()
            draw_cell(c0.getX(), c0.getY(), "red", "R")

        # agentes
        for a in self.agents:
            c0 = a.getCoord()
            draw_cell(c0.getX(), c0.getY(), "lightgreen", "A")
