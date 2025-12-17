import tkinter as tk

# --------------------------
# RENDER GRÁFICO COM TKINTER
# --------------------------



def init_render_window(self):
    

    if hasattr(self, "root") and self.root.winfo_exists():
        return   # JÁ EXISTE → não cria outra

    self.window_closed = False
    self.CELL = 30
    w, h = self.grid_size

    self.root = tk.Tk()
    self.root.title("Grid")
    self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    self.canvas = tk.Canvas(
        self.root,
        width=w * self.CELL,
        height=h * self.CELL,
        bg="white"
    )
    self.canvas.pack()



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
        
        '''
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        COLORS SHOULD NOT BE DEFINED HERE
        '''
        
        color = {
            "Wall": "black",
            "Fireplace": "orange",
            "Limit": "gray",
            "Border": "gray"
        }.get(t, "brown")
        draw_cell(coord.getX(), coord.getY(), color)

    # farol
    if self.lighthouse:
        c0 = self.lighthouse.getCoord()
        draw_cell(c0.getX(), c0.getY(), "yellow", "L")

    # agentes
    for a in self.agents:
        c0 = a.getCoord()
        draw_cell(c0.getX(), c0.getY(), "lightgreen", "A")


def _on_close(self):
    self.window_closed = True
    self.root.destroy()






